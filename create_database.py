import docx
import json
import re
from sentence_transformers import SentenceTransformer
import numpy as np

def extract_text_from_docx(file_path):
    """Extract text from DOCX file"""
    doc = docx.Document(file_path)
    full_text = []
    
    for para in doc.paragraphs:
        if para.text.strip():
            full_text.append(para.text.strip())
    
    return full_text

def create_chunks(text_list, chunk_size=200):
    """Create chunks of text for RAG processing"""
    chunks = []
    current_chunk = ""
    
    for text in text_list:
        # If adding this text would exceed chunk size, save current chunk
        if len(current_chunk + " " + text) > chunk_size and current_chunk:
            chunks.append(current_chunk.strip())
            current_chunk = text
        else:
            current_chunk += " " + text if current_chunk else text
    
    # Add the last chunk
    if current_chunk:
        chunks.append(current_chunk.strip())
    
    return chunks

def categorize_content(text):
    """Categorize content based on keywords"""
    text_lower = text.lower()
    
    if any(keyword in text_lower for keyword in ['service', 'solution', 'consulting', 'development']):
        return 'services'
    elif any(keyword in text_lower for keyword in ['about', 'company', 'founded', 'mission', 'vision']):
        return 'company_info'
    elif any(keyword in text_lower for keyword in ['contact', 'email', 'phone', 'address']):
        return 'contact'
    elif any(keyword in text_lower for keyword in ['technology', 'tech', 'ai', 'machine learning', 'data']):
        return 'technology'
    elif any(keyword in text_lower for keyword in ['team', 'employee', 'staff', 'expert']):
        return 'team'
    else:
        return 'general'

def create_rag_database():
    """Create RAG database from the DOCX file"""
    
    # Extract text from document
    document_path = "MachDatum Details.docx"
    text_list = extract_text_from_docx(document_path)
    
    # Create chunks
    chunks = create_chunks(text_list, chunk_size=300)
    
    # Initialize sentence transformer for embeddings
    model = SentenceTransformer('all-MiniLM-L6-v2')
    
    # Create database entries
    database = {
        "company_name": "MachDatum",
        "website": "https://www.machdatum.com/",
        "knowledge_base": []
    }
    
    for i, chunk in enumerate(chunks):
        if len(chunk.strip()) < 20:  # Skip very short chunks
            continue
            
        # Generate embedding
        embedding = model.encode(chunk)
        
        # Create database entry
        entry = {
            "id": i + 1,
            "content": chunk,
            "category": categorize_content(chunk),
            "embedding": embedding.tolist(),  # Convert numpy array to list for JSON serialization
            "metadata": {
                "length": len(chunk),
                "word_count": len(chunk.split())
            }
        }
        
        database["knowledge_base"].append(entry)
    
    # Save to JSON file
    with open('machdatum_rag_db.json', 'w', encoding='utf-8') as f:
        json.dump(database, f, indent=2, ensure_ascii=False)
    
    print(f"Created RAG database with {len(database['knowledge_base'])} entries")
    return database

if __name__ == "__main__":
    create_rag_database()
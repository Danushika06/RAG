import os
import sys
from create_database import create_rag_database

def ensure_database_exists():
    """Ensure the RAG database exists, create it if it doesn't"""
    db_path = "machdatum_rag_db.json"
    
    if not os.path.exists(db_path):
        print("Database file not found. Creating RAG database...")
        try:
            # Check if the source document exists
            if os.path.exists("MachDatum Details.docx"):
                create_rag_database()
                print("RAG database created successfully!")
            else:
                print("Warning: MachDatum Details.docx not found. Cannot create database.")
                # Create a minimal database for testing
                import json
                minimal_db = {
                    "metadata": {
                        "created_at": "auto-generated",
                        "total_entries": 1,
                        "source_document": "fallback"
                    },
                    "knowledge_base": [
                        {
                            "id": 1,
                            "content": "This is a RAG chatbot for MachDatum company. Please upload the company documents to create a proper knowledge base.",
                            "category": "General",
                            "embedding": [0.0] * 384,  # Placeholder embedding
                            "metadata": {
                                "length": 100,
                                "word_count": 20
                            }
                        }
                    ]
                }
                with open(db_path, 'w', encoding='utf-8') as f:
                    json.dump(minimal_db, f, indent=2, ensure_ascii=False)
                print("Created minimal database for testing.")
        except Exception as e:
            print(f"Error creating database: {e}")
            return False
    else:
        print("Database file exists.")
    
    return True

if __name__ == "__main__":
    ensure_database_exists()
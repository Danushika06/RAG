import json
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import google.generativeai as genai
import os
from typing import List, Dict, Any

class RAGChatbot:
    def __init__(self, db_path: str, gemini_api_key: str):
        """Initialize RAG Chatbot"""
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.gemini_api_key = gemini_api_key
        
        # Configure Gemini API
        genai.configure(api_key=gemini_api_key)
        
        # Load database
        self.load_database(db_path)
        
    def load_database(self, db_path: str):
        """Load the RAG database"""
        with open(db_path, 'r', encoding='utf-8') as f:
            self.database = json.load(f)
        
        # Convert embeddings back to numpy arrays
        for entry in self.database['knowledge_base']:
            entry['embedding'] = np.array(entry['embedding'])
            
        print(f"Loaded database with {len(self.database['knowledge_base'])} entries")
    
    def find_similar_context(self, query: str, top_k: int = 3, similarity_threshold: float = 0.3) -> List[Dict[Any, Any]]:
        """Find similar context from the database"""
        
        # Generate embedding for the query
        query_embedding = self.model.encode([query])
        
        # Calculate similarities
        similarities = []
        for entry in self.database['knowledge_base']:
            similarity = cosine_similarity(query_embedding, [entry['embedding']])[0][0]
            if similarity >= similarity_threshold:
                similarities.append({
                    'entry': entry,
                    'similarity': similarity
                })
        
        # Sort by similarity and return top_k
        similarities.sort(key=lambda x: x['similarity'], reverse=True)
        return similarities[:top_k]
    
    def generate_response(self, query: str, context_entries: List[Dict[Any, Any]]) -> str:
        """Generate response using Gemini API with context"""
        
        # Prepare context
        context_text = "\n\n".join([entry['entry']['content'] for entry in context_entries])
        
        # Create prompt
        prompt = f"""You are a helpful assistant for MachDatum company. Use the following context information to answer the user's question. If the context doesn't contain relevant information, politely say so and provide general guidance.

Context Information:
{context_text}

User Question: {query}

Please provide a helpful, accurate, and professional response based on the context. If you're referencing specific information from the context, make sure it's accurate."""

        try:
            # Generate response with Gemini using the older API
            response = genai.generate_text(
                model='models/text-bison-001',
                prompt=prompt,
                temperature=0.7,
                max_output_tokens=800
            )
            return response.result if response.result else "I apologize, but I couldn't generate a proper response. Please try rephrasing your question."
        except Exception as e:
            return f"I apologize, but I encountered an error while generating a response: {str(e)}. Please try rephrasing your question."
    
    def chat(self, user_input: str) -> Dict[str, Any]:
        """Main chat function"""
        
        # Find similar context
        similar_contexts = self.find_similar_context(user_input, top_k=3)
        
        if not similar_contexts:
            return {
                "response": "I don't have specific information about that topic in my knowledge base. Could you please rephrase your question or ask about MachDatum's services, company information, or contact details?",
                "context_used": [],
                "similarity_scores": []
            }
        
        # Generate response
        response = self.generate_response(user_input, similar_contexts)
        
        return {
            "response": response,
            "context_used": [entry['entry']['content'][:200] + "..." for entry in similar_contexts],
            "similarity_scores": [entry['similarity'] for entry in similar_contexts]
        }

def main():
    """Test the chatbot"""
    
    # Initialize chatbot
    api_key = "AIzaSyB7rOwEQeZTS4y_Zhz3sFjRMeoEpcPLQtw"
    chatbot = RAGChatbot("machdatum_rag_db.json", api_key)
    
    print("MachDatum RAG Chatbot initialized!")
    print("Type 'quit' to exit")
    print("-" * 50)
    
    while True:
        user_input = input("\nYou: ").strip()
        
        if user_input.lower() in ['quit', 'exit', 'bye']:
            print("Goodbye!")
            break
            
        if not user_input:
            continue
            
        # Get response
        result = chatbot.chat(user_input)
        
        print(f"\nBot: {result['response']}")
        
        # Show debug info
        if result['context_used']:
            print(f"\n[Debug] Used {len(result['context_used'])} context entries with similarities: {[f'{score:.3f}' for score in result['similarity_scores']]}")

if __name__ == "__main__":
    main()
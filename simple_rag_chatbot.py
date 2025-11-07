import json
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from typing import List, Dict, Any

class SimpleRAGChatbot:
    def __init__(self, db_path: str):
        """Initialize Simple RAG Chatbot without LLM"""
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        
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
    
    def generate_simple_response(self, query: str, context_entries: List[Dict[Any, Any]]) -> str:
        """Generate a simple response based on context"""
        
        if not context_entries:
            return "I don't have specific information about that topic in my knowledge base. Could you please rephrase your question or ask about MachDatum's services, company information, or contact details?"
        
        # Analyze query type for better formatting
        query_lower = query.lower()
        
        # Create formatted response based on context
        response_parts = []
        
        if any(word in query_lower for word in ['service', 'services', 'offer', 'provide', 'solution']):
            response_parts.append("## MachDatum Services & Solutions")
        elif any(word in query_lower for word in ['contact', 'reach', 'email', 'phone', 'address']):
            response_parts.append("## Contact Information")
        elif any(word in query_lower for word in ['team', 'people', 'staff', 'who', 'member']):
            response_parts.append("## Team Information")
        elif any(word in query_lower for word in ['about', 'company', 'background', 'history']):
            response_parts.append("## About MachDatum")
        elif any(word in query_lower for word in ['technology', 'tech', 'tools', 'platform']):
            response_parts.append("## Technologies & Platforms")
        else:
            response_parts.append("## Information Found")
        
        # Add formatted content
        for i, entry in enumerate(context_entries, 1):
            content = entry['entry']['content'].strip()
            
            # Format content based on type
            if 'email' in content.lower() or 'phone' in content.lower() or 'contact' in content.lower():
                # Contact information formatting
                lines = content.split('\n')
                formatted_lines = []
                for line in lines:
                    line = line.strip()
                    if line:
                        if '@' in line:
                            formatted_lines.append(f"📧 **Email:** {line}")
                        elif any(char.isdigit() for char in line) and len(line) > 8:
                            formatted_lines.append(f"📞 **Phone:** {line}")
                        else:
                            formatted_lines.append(f"• {line}")
                response_parts.append('\n'.join(formatted_lines))
            
            elif any(word in content.lower() for word in ['ceo', 'director', 'lead', 'engineer', 'manager']):
                # Team member formatting
                lines = content.split('\n')
                formatted_lines = []
                current_person = ""
                for line in lines:
                    line = line.strip()
                    if line:
                        if any(title in line.lower() for title in ['ceo', 'director', 'lead', 'engineer', 'manager', 'sde']):
                            if current_person:
                                formatted_lines.append(current_person)
                            # Split name and title
                            parts = line.split(' ')
                            if len(parts) >= 3:
                                name = ' '.join(parts[:-2]) if len(parts) > 3 else ' '.join(parts[:-1])
                                title = ' '.join(parts[-2:]) if len(parts) > 3 else parts[-1]
                                current_person = f"👤 **{name}** - *{title}*"
                            else:
                                current_person = f"👤 **{line}**"
                        else:
                            if current_person:
                                formatted_lines.append(current_person)
                                current_person = ""
                            formatted_lines.append(f"• {line}")
                
                if current_person:
                    formatted_lines.append(current_person)
                
                response_parts.append('\n'.join(formatted_lines))
            
            elif 'service' in content.lower() or 'solution' in content.lower():
                # Service formatting
                lines = content.split('.')
                formatted_lines = []
                for line in lines:
                    line = line.strip()
                    if line and len(line) > 10:
                        formatted_lines.append(f"🔹 {line}")
                response_parts.append('\n'.join(formatted_lines))
            
            else:
                # General formatting
                sentences = content.split('.')
                formatted_sentences = []
                for sentence in sentences:
                    sentence = sentence.strip()
                    if sentence and len(sentence) > 5:
                        formatted_sentences.append(f"• {sentence}")
                response_parts.append('\n'.join(formatted_sentences))
        
        # Add footer
        response_parts.append("\n---")
        response_parts.append("💡 *Need more specific information? Feel free to ask about any particular aspect!*")
        
        return '\n\n'.join(response_parts)
    
    def chat(self, user_input: str) -> Dict[str, Any]:
        """Main chat function"""
        
        # Find similar context
        similar_contexts = self.find_similar_context(user_input, top_k=3)
        
        # Generate response
        response = self.generate_simple_response(user_input, similar_contexts)
        
        return {
            "response": response,
            "context_used": [entry['entry']['content'][:200] + "..." if len(entry['entry']['content']) > 200 else entry['entry']['content'] for entry in similar_contexts],
            "similarity_scores": [entry['similarity'] for entry in similar_contexts]
        }

def main():
    """Test the simple chatbot"""
    
    # Initialize chatbot
    chatbot = SimpleRAGChatbot("machdatum_rag_db.json")
    
    print("MachDatum Simple RAG Chatbot initialized!")
    print("This version shows you the retrieved context information.")
    print("Type 'quit' to exit")
    print("-" * 60)
    
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
            print(f"\n[Debug] Found {len(result['context_used'])} relevant context entries with similarities: {[f'{score:.3f}' for score in result['similarity_scores']]}")

if __name__ == "__main__":
    main()
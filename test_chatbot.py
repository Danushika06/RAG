from rag_chatbot import RAGChatbot

# Test the RAG chatbot
def test_chatbot():
    # Initialize chatbot
    api_key = 'AIzaSyB7rOwEQeZTS4y_Zhz3sFjRMeoEpcPLQtw'
    chatbot = RAGChatbot('machdatum_rag_db.json', api_key)
    
    # Test questions
    test_questions = [
        "What services does MachDatum provide?",
        "How can I contact MachDatum?", 
        "Tell me about the company",
        "What technologies do you work with?"
    ]
    
    print("=== MachDatum RAG Chatbot Test ===\n")
    
    for i, question in enumerate(test_questions, 1):
        print(f"Test {i}: {question}")
        print("-" * 50)
        
        try:
            result = chatbot.chat(question)
            print(f"Response: {result['response']}")
            print(f"Context entries used: {len(result['context_used'])}")
            if result['similarity_scores']:
                scores = [f"{score:.3f}" for score in result['similarity_scores']]
                print(f"Similarity scores: {scores}")
            print()
        except Exception as e:
            print(f"Error: {e}")
            print()

if __name__ == "__main__":
    test_chatbot()
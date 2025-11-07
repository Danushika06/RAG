from rag_chatbot import RAGChatbot

# Test one question with Gemini API
try:
    print("Testing Gemini API integration...")
    api_key = 'AIzaSyB7rOwEQeZTS4y_Zhz3sFjRMeoEpcPLQtw'
    chatbot = RAGChatbot('machdatum_rag_db.json', api_key)
    
    question = "What services does MachDatum provide?"
    print(f"Question: {question}")
    
    result = chatbot.chat(question)
    print(f"Response: {result['response']}")
    print(f"Context entries used: {len(result['context_used'])}")
    
except Exception as e:
    print(f"Error: {e}")
    print("\nFalling back to simple chatbot without LLM...")
    
    # Use simple version as backup
    from simple_rag_chatbot import SimpleRAGChatbot
    simple_chatbot = SimpleRAGChatbot('machdatum_rag_db.json')
    result = simple_chatbot.chat(question)
    print(f"Simple Response: {result['response']}")
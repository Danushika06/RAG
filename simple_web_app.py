from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from simple_rag_chatbot import SimpleRAGChatbot
import os
from dotenv import load_dotenv

# Load environment variables
try:
    load_dotenv()
except:
    pass  # dotenv not available

app = Flask(__name__)
CORS(app)

# Initialize chatbot
FLASK_PORT = int(os.getenv('FLASK_PORT', 5000))
FLASK_DEBUG = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'

chatbot = None

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    global chatbot
    
    try:
        data = request.json
        user_message = data.get('message', '')
        
        if not user_message:
            return jsonify({'error': 'No message provided'}), 400
        
        # Initialize chatbot if not already done
        if chatbot is None:
            chatbot = SimpleRAGChatbot("machdatum_rag_db.json")
        
        # Get response
        result = chatbot.chat(user_message)
        
        return jsonify({
            'response': result['response'],
            'context_count': len(result['context_used']),
            'similarity_scores': result['similarity_scores']
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health')
def health():
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    print("🚀 Starting MachDatum RAG Chatbot Web Interface...")
    print(f"📁 Database: machdatum_rag_db.json")
    print(f"🌐 URL: http://localhost:{FLASK_PORT}")
    print("💡 Note: This version uses rule-based responses with RAG context")
    print("-" * 60)
    app.run(debug=FLASK_DEBUG, host='0.0.0.0', port=FLASK_PORT)
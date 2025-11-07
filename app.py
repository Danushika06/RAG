from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from rag_chatbot import RAGChatbot
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Initialize chatbot
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', 'AIzaSyB7rOwEQeZTS4y_Zhz3sFjRMeoEpcPLQtw')
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
            chatbot = RAGChatbot("machdatum_rag_db.json", GEMINI_API_KEY)
        
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
    app.run(debug=FLASK_DEBUG, host='0.0.0.0', port=FLASK_PORT)
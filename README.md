# MachDatum RAG Chatbot

A Retrieval-Augmented Generation (RAG) chatbot for MachDatum company that uses document-based knowledge retrieval and Google's Gemini API to provide intelligent responses about the company.

## Features

- 📄 **Document Processing**: Extracts and processes content from Word documents
- 🔍 **Semantic Search**: Uses sentence transformers for finding relevant context
- 🤖 **AI Response Generation**: Integrates with Google Gemini API for intelligent responses
- 💬 **Web Interface**: Beautiful, responsive web interface for easy interaction
- 🖥️ **CLI Interface**: Command-line interface for direct testing
- 📊 **Context Tracking**: Shows similarity scores and context usage

## Project Structure

```
rag/
├── MachDatum Details.docx      # Source document with company information
├── create_database.py          # Script to create RAG database from document
├── rag_chatbot.py             # Main RAG chatbot implementation
├── app.py                     # Flask web application
├── templates/
│   └── index.html             # Web interface template
├── requirements.txt           # Python dependencies
├── setup_and_run.py          # Automated setup and run script
├── run.bat                    # Windows batch script to run everything
├── .env                       # Environment configuration
└── README.md                  # This file
```

## Quick Start

### Option 1: Automated Setup (Recommended)

1. **Run the setup script:**
   ```bash
   python setup_and_run.py
   ```
   
   This will:
   - Install all dependencies
   - Create the RAG database from the document
   - Give you options to run web interface or CLI

### Option 2: Manual Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Create the RAG database:**
   ```bash
   python create_database.py
   ```

3. **Run the application:**
   
   For web interface:
   ```bash
   python app.py
   ```
   Then open http://localhost:5000 in your browser
   
   For command-line interface:
   ```bash
   python rag_chatbot.py
   ```

### Option 3: Windows Batch File

Simply double-click `run.bat` or run:
```cmd
run.bat
```

## How It Works

### 1. Document Processing
- Reads the MachDatum Details.docx file
- Splits content into semantic chunks
- Categorizes content (services, company info, contact, etc.)
- Generates embeddings for each chunk using sentence transformers

### 2. RAG Database Structure
```json
{
  "company_name": "MachDatum",
  "website": "https://www.machdatum.com/",
  "knowledge_base": [
    {
      "id": 1,
      "content": "Text chunk content...",
      "category": "services",
      "embedding": [0.1, 0.2, ...],
      "metadata": {
        "length": 250,
        "word_count": 42
      }
    }
  ]
}
```

### 3. Query Processing
- User query is converted to embedding
- Cosine similarity search finds relevant context
- Top-K most similar chunks are retrieved
- Context is sent to Gemini API with the user query
- AI generates contextual response

## Configuration

Edit `.env` file to customize settings:

```env
GEMINI_API_KEY=your_gemini_api_key
FLASK_PORT=5000
FLASK_DEBUG=True
CHUNK_SIZE=300
TOP_K_RESULTS=3
SIMILARITY_THRESHOLD=0.3
```

## API Endpoints

### Web Application
- `GET /` - Web interface
- `POST /chat` - Chat endpoint
- `GET /health` - Health check

### Chat API Usage
```bash
curl -X POST http://localhost:5000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What services does MachDatum offer?"}'
```

## Example Queries

Try asking the chatbot:

- "What services does MachDatum provide?"
- "How can I contact MachDatum?"
- "Tell me about the company's background"
- "What technologies does MachDatum work with?"
- "Who are the team members?"

## Dependencies

- `google-generativeai`: Google Gemini API integration
- `python-docx`: Word document processing
- `sentence-transformers`: Text embedding generation
- `scikit-learn`: Similarity calculations
- `flask`: Web framework
- `flask-cors`: CORS support
- `python-dotenv`: Environment variable management

## Troubleshooting

### Common Issues

1. **Import errors**: Make sure all dependencies are installed
   ```bash
   pip install -r requirements.txt
   ```

2. **Document not found**: Ensure `MachDatum Details.docx` is in the project directory

3. **Gemini API errors**: Verify your API key is correct and has quota available

4. **Memory issues**: Reduce `CHUNK_SIZE` in configuration for large documents

### Debug Information

The web interface shows:
- Number of context entries used
- Similarity scores for retrieved context
- This helps understand how the RAG system is working

## Customization

### Adding More Documents
1. Process additional documents in `create_database.py`
2. Combine embeddings in the knowledge base
3. Update categorization logic if needed

### Improving Context Retrieval
- Adjust `SIMILARITY_THRESHOLD` for more/fewer results
- Modify `TOP_K_RESULTS` for different context amounts
- Experiment with different sentence transformer models

### Enhancing UI
- Modify `templates/index.html` for different styling
- Add features like conversation history
- Implement user authentication if needed

## License

This project is created for MachDatum company internal use.

## Support

For issues or questions about this RAG chatbot implementation, please check the troubleshooting section or review the code comments for detailed explanations.
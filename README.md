# Personal AI Assistant - Jarvis

A self-hosted, LLM-powered personal assistant that understands user queries and responds with contextually relevant information. Built with modern technologies for knowledge retrieval and conversational AI.

## 🚀 Features

- **Self-hosted LLM**: Uses LLaMA (or compatible GGUF models) for privacy and control
- **Vector Database**: Pinecone integration for semantic search and knowledge retrieval
- **RAG (Retrieval Augmented Generation)**: Combines LLM with knowledge base for contextual responses
- **Knowledge Management**: Create, update, and manage knowledge entries
- **Conversational UI**: Modern React-based chatbot interface
- **Semantic Search**: Find relevant knowledge using embeddings
- **REST API**: Complete API for all operations

## 📋 Prerequisites

- Python 3.9+
- Node.js 16+ and npm/yarn
- Pinecone account (free tier available)
- 4GB+ RAM (8GB+ recommended for LLM)
- macOS/Linux/Windows

## 🛠️ Installation

### Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env
```

### Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install
```

## ⚙️ Configuration

### Backend Configuration (.env)

Edit `backend/.env` with your settings:

```env
# Pinecone Configuration
PINECONE_API_KEY=your_pinecone_api_key
PINECONE_ENVIRONMENT=your_pinecone_environment
PINECONE_INDEX_NAME=jarvis-index

# LLM Configuration
LLM_MODEL_PATH=./models/llama-2-7b-chat.gguf
LLM_CONTEXT_WINDOW=2048
LLM_MAX_TOKENS=512
LLM_TEMPERATURE=0.7

# Embedding Model
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
CORS_ORIGINS=["http://localhost:3000", "http://localhost:5173"]
```

### Download LLaMA Model

1. Visit [TheBloke's Hugging Face](https://huggingface.co/TheBloke)
2. Download a GGUF quantized model (e.g., `llama-2-7b-chat.gguf`)
3. Place in `backend/models/` directory

Example:
```bash
mkdir -p backend/models
# Download model file to backend/models/
```

## 🚀 Running the Application

### Terminal 1: Backend

```bash
cd backend
source venv/bin/activate
python main.py
```

Backend will start at `http://localhost:8000`

### Terminal 2: Frontend

```bash
cd frontend
npm run dev
```

Frontend will start at `http://localhost:5173`

## 📚 API Endpoints

### Chat
- `POST /chat` - Send a query and get assistant response
  - Includes RAG with knowledge base retrieval
  - Returns response, sources, and confidence score

### Knowledge Management
- `GET /knowledge` - Get all knowledge entries
- `POST /knowledge` - Add new knowledge entry
- `GET /knowledge/{id}` - Get specific entry
- `PUT /knowledge/{id}` - Update entry
- `DELETE /knowledge/{id}` - Delete entry
- `POST /search` - Search knowledge base

### Health
- `GET /health` - Check component status

## 🧠 How It Works

1. **User Query**: User sends a message through the UI
2. **Embedding Generation**: Query is converted to embedding vector
3. **Vector Search**: Pinecone searches for similar knowledge entries
4. **Context Building**: Retrieved entries become context for the LLM
5. **Response Generation**: LLaMA generates response based on context
6. **Response Display**: Assistant response with sources shown to user

## 📖 Usage Examples

### Add Knowledge Entry
```bash
curl -X POST http://localhost:8000/knowledge \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Python Tips",
    "content": "Always use virtual environments for Python projects",
    "category": "technical",
    "tags": ["python", "best-practices"]
  }'
```

### Chat with Assistant
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "query": "How do I use virtual environments?",
    "conversation_history": []
  }'
```

### Search Knowledge Base
```bash
curl -X POST http://localhost:8000/search \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Python best practices",
    "top_k": 5
  }'
```

## 🏗️ Project Structure

```
tropic/
├── backend/
│   ├── main.py                 # FastAPI application
│   ├── config.py               # Configuration management
│   ├── llm_manager.py          # LLaMA model handling
│   ├── embedding_manager.py    # Text embeddings
│   ├── vector_db.py            # Pinecone integration
│   ├── knowledge_base.py       # Knowledge storage
│   ├── models.py               # Pydantic models
│   ├── requirements.txt        # Python dependencies
│   └── .env.example            # Example environment
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── ChatInterface.jsx      # Chat UI
│   │   │   └── KnowledgeManager.jsx   # Knowledge management
│   │   ├── api.js              # API client
│   │   ├── App.jsx             # Main component
│   │   ├── main.jsx            # Entry point
│   │   └── index.css           # Styling
│   ├── index.html              # HTML template
│   ├── package.json            # Dependencies
│   ├── vite.config.js          # Vite config
│   └── tailwind.config.js      # Tailwind config
│
├── data/
│   └── knowledge_base.json     # Local knowledge storage
│
└── README.md                    # This file
```

## 🔧 Troubleshooting

### Model Not Loading
- Ensure GGUF model file exists at configured path
- Check file permissions
- Verify llama-cpp-python installation

### Pinecone Connection Issues
- Verify API key and environment
- Check internet connection
- Ensure index name is correct

### Embedding Model Not Available
- Run: `pip install sentence-transformers`
- Check disk space for model downloads

### CORS Errors
- Verify CORS_ORIGINS in .env includes frontend URL
- Check frontend API endpoint configuration

## 🚀 Advanced Configuration

### Using Different LLM Models
Replace `LLM_MODEL_PATH` with path to any GGUF format model:
- Mistral 7B
- Neural Chat
- Dolphin
- Wizard models

### Custom Embedding Model
Change `EMBEDDING_MODEL` to any Hugging Face sentence-transformers model

### Production Deployment
1. Use environment variables for sensitive data
2. Run behind a reverse proxy (nginx)
3. Use proper database for knowledge storage
4. Implement authentication/authorization
5. Use HTTPS with valid certificates
6. Scale with multiple API instances

## 📝 License

MIT License - Feel free to use for personal or commercial projects

## 🤝 Contributing

Contributions welcome! Please feel free to submit pull requests.

## 📞 Support

For issues and questions:
1. Check troubleshooting section
2. Review logs for error messages
3. Consult API documentation

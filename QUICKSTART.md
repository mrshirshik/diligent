# Getting Started Guide

## 📦 Installation & Setup

### Step 1: Quick Setup
The easiest way to get started:

```bash
cd /Users/kishanshirshikk/Downloads/tropic
chmod +x setup.sh start.sh
./setup.sh
```

This will:
- Create Python virtual environment
- Install all Python dependencies
- Install Node.js dependencies
- Create `.env` file from template

### Step 2: Configure Your Environment

Edit `backend/.env`:

```bash
# Get your free Pinecone API key from https://www.pinecone.io/
PINECONE_API_KEY=your_key_here
PINECONE_ENVIRONMENT=us-east-1-aws  # Your environment
```

### Step 3: Download LLaMA Model

Download a GGUF quantized model (e.g., 7B parameters for lower RAM requirements):

```bash
# Create models directory
mkdir -p backend/models

# Download llama-2-7b-chat model (~4GB)
# From: https://huggingface.co/TheBloke/Llama-2-7B-chat-GGUF/
# Or use any other GGUF format model
```

### Step 4: Start the Application

```bash
./start.sh
```

This starts both backend and frontend servers. Open your browser:
- **Chat Interface**: http://localhost:5173
- **API Docs**: http://localhost:8000/docs

## 🎯 First Steps

### 1. Add Knowledge Entries
- Navigate to "Knowledge Base" tab in the UI
- Click "Add Entry"
- Fill in title, content, category, and tags
- Submit

### 2. Chat with Jarvis
- Go to "Chat" tab
- Ask a question related to your knowledge entries
- Jarvis will search your knowledge base and provide contextual responses

### 3. Monitor System Health
- Check the status indicator in the top-right of the chat interface
- Visit http://localhost:8000/health for API status

## 📚 Key Components

### Backend (Python + FastAPI)
- **LLM Manager**: Handles LLaMA model inference
- **Embedding Manager**: Converts text to vectors
- **Vector DB**: Pinecone integration for semantic search
- **Knowledge Base**: Local JSON storage for entries
- **REST API**: All operations exposed via HTTP

### Frontend (React + Vite)
- **Chat Interface**: Beautiful conversational UI
- **Knowledge Manager**: Create, edit, delete, search entries
- **API Client**: Communicates with backend

### Infrastructure
- **Pinecone**: Vector database (free tier available)
- **Sentence Transformers**: Embedding model
- **LLaMA 2**: Self-hosted language model

## 🔧 Customization

### Use a Different LLM Model
1. Download different GGUF model
2. Update `LLM_MODEL_PATH` in `.env`
3. Restart backend

Recommended models:
- Llama 2 (7B, 13B, 70B)
- Mistral 7B
- Neural Chat
- Wizard LM

### Change Embedding Model
Update `EMBEDDING_MODEL` in `.env`:
- `all-MiniLM-L6-v2` (default, fast)
- `all-mpnet-base-v2` (better quality, slower)
- `multilingual-e5-large` (multilingual)

### Adjust LLM Parameters
In `.env`:
- `LLM_CONTEXT_WINDOW`: How much text context to consider
- `LLM_MAX_TOKENS`: Maximum response length
- `LLM_TEMPERATURE`: 0-1, lower=more deterministic, higher=more creative

## 🚀 Production Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for:
- Docker containerization
- Cloud deployment options
- SSL/HTTPS setup
- Load balancing
- Monitoring and logging

## 🐛 Troubleshooting

### "Model not found" error
```bash
# Check if model file exists
ls -lh backend/models/

# Download model to correct location
# Model should be: backend/models/llama-2-7b-chat.gguf
```

### "Pinecone API key invalid"
```bash
# Verify .env file has correct key
cat backend/.env | grep PINECONE_API_KEY

# Get new key from https://www.pinecone.io/
```

### "Port 8000 already in use"
```bash
# Find process using port
lsof -i :8000

# Change API_PORT in .env
API_PORT=8001
```

### Frontend can't connect to backend
```bash
# Check CORS_ORIGINS in backend/.env
# Should include frontend URL:
CORS_ORIGINS=["http://localhost:5173"]

# Restart backend
```

## 📖 Full Documentation

- [API Reference](API.md) - Detailed API endpoints
- [Deployment Guide](DEPLOYMENT.md) - Production setup
- [README.md](README.md) - Project overview

## 💡 Tips & Tricks

### Populate with Sample Data
```bash
cd backend
python ../populate_kb.py
```

### Access OpenAPI Docs
Visit `http://localhost:8000/docs` for interactive API documentation

### Export Knowledge Base
```bash
cat data/knowledge_base.json > backup.json
```

### Monitor Backend Logs
```bash
# Terminal with backend running
# Logs appear in real-time
```

### Test API from Command Line
```bash
# Chat
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "Hello Jarvis"}'

# Add knowledge
curl -X POST http://localhost:8000/knowledge \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Test",
    "content": "Test content",
    "category": "general"
  }'
```

## 🎓 Learning Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev/)
- [Pinecone Docs](https://docs.pinecone.io/)
- [LLaMA Model Info](https://llama.meta.com/)
- [RAG Pattern](https://docs.anthropic.com/en/docs/build-a-chatbot)

## 🤝 Need Help?

1. Check the troubleshooting section above
2. Review logs for error details
3. Visit [API.md](API.md) for endpoint details
4. Check component status with `/health` endpoint

## 🎉 You're All Set!

You now have a fully functional personal AI assistant. Start by:
1. Adding knowledge entries
2. Asking questions
3. Customizing the system
4. Deploying to production

Happy coding! 🚀

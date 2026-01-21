# Project Structure

```
tropic/
├── backend/                          # Python FastAPI backend
│   ├── main.py                      # Main FastAPI application
│   ├── config.py                    # Configuration management
│   ├── llm_manager.py               # LLaMA model integration
│   ├── embedding_manager.py         # Text embedding handler
│   ├── vector_db.py                 # Pinecone integration
│   ├── knowledge_base.py            # Knowledge storage & retrieval
│   ├── models.py                    # Pydantic data models
│   ├── requirements.txt             # Python dependencies
│   ├── .env.example                 # Environment variables template
│   ├── .gitignore                   # Git ignore rules
│   └── models/                      # LLaMA model directory (not in repo)
│       └── llama-2-7b-chat.gguf    # GGUF format model
│
├── frontend/                         # React + Vite frontend
│   ├── src/
│   │   ├── components/
│   │   │   ├── ChatInterface.jsx    # Main chat component
│   │   │   └── KnowledgeManager.jsx # Knowledge management UI
│   │   ├── api.js                   # Axios API client
│   │   ├── App.jsx                  # Root component
│   │   ├── main.jsx                 # React entry point
│   │   └── index.css                # Tailwind CSS imports
│   ├── public/
│   ├── index.html                   # HTML template
│   ├── package.json                 # Node.js dependencies
│   ├── vite.config.js               # Vite configuration
│   ├── tailwind.config.js           # Tailwind CSS config
│   ├── postcss.config.js            # PostCSS config
│   └── .gitignore                   # Git ignore rules
│
├── data/                            # Data directory
│   └── knowledge_base.json          # Local knowledge storage
│
├── .gitignore                       # Root git ignore
├── README.md                        # Project overview
├── QUICKSTART.md                    # Getting started guide
├── API.md                           # API documentation
├── DEPLOYMENT.md                    # Deployment guide
├── ARCHITECTURE.md                  # This file
├── setup.sh                         # Setup automation script
├── start.sh                         # Start both services
├── populate_kb.py                   # Sample data population
└── examples.py                      # Advanced usage examples
```

## Component Overview

### Backend Architecture

```
┌─────────────────────────────────────────┐
│         FastAPI Application             │
│        (main.py - Port 8000)            │
└──────────┬──────────────────────────────┘
           │
    ┌──────┴──────────────────────────────────┐
    │                                          │
    ├─ Chat Endpoint                          │
    │  ├─ LLMManager                          │
    │  │   └─ llama-cpp-python               │
    │  │       └─ GGUF Model                  │
    │  │                                      │
    │  ├─ EmbeddingManager                    │
    │  │   └─ sentence-transformers           │
    │  │       └─ all-MiniLM-L6-v2           │
    │  │                                      │
    │  └─ VectorDBManager                     │
    │      └─ Pinecone (Semantic Search)     │
    │                                        │
    ├─ Knowledge Endpoints                   │
    │  ├─ GET /knowledge                     │
    │  ├─ POST /knowledge                    │
    │  ├─ PUT /knowledge/{id}                │
    │  ├─ DELETE /knowledge/{id}             │
    │  └─ POST /search                       │
    │                                        │
    └─ Health Check                          │
       └─ GET /health                        │
```

### Frontend Architecture

```
┌────────────────────────────────────────┐
│    React Application (Port 5173)       │
│         Vite Dev Server                │
└────────┬───────────────────────────────┘
         │
    ┌────┴─────────────────────────────┐
    │                                   │
    ├─ App.jsx (Router)                │
    │  ├─ ChatInterface Component      │
    │  │  ├─ Message Display           │
    │  │  ├─ Input Area                │
    │  │  └─ Source Display            │
    │  │                               │
    │  └─ KnowledgeManager Component  │
    │     ├─ Entry List                │
    │     ├─ Add Form                  │
    │     ├─ Edit Form                 │
    │     └─ Search                    │
    │                                  │
    └─ API Client (api.js)            │
       └─ Axios HTTP Client           │
```

### Data Flow: User Query to Response

```
User Input
    │
    ├─→ [Frontend] ChatInterface.jsx
    │   └─→ Sends query via api.js
    │
    ├─→ [Backend] POST /chat endpoint
    │   ├─ EmbeddingManager converts query to vector
    │   │
    │   ├─ VectorDBManager searches Pinecone
    │   │  └─ Returns similar knowledge entries
    │   │
    │   ├─ Build context from retrieved entries
    │   │
    │   ├─ LLMManager generates response
    │   │  └─ Uses LLaMA with context
    │   │
    │   └─ Return response + sources + confidence
    │
    └─→ [Frontend] Display response
        ├─ Show assistant message
        ├─ Display source references
        └─ Show confidence score
```

### Vector Database Flow

```
Knowledge Entry
    │
    ├─→ EmbeddingManager
    │   └─→ Text → Vector (384 dimensions)
    │
    ├─→ VectorDBManager
    │   └─→ Pinecone.upsert()
    │
    └─→ Stored in Pinecone Index
        └─→ Namespace: "knowledge"
            └─→ Indexed by vector similarity

User Query
    │
    ├─→ EmbeddingManager
    │   └─→ Query → Vector
    │
    ├─→ VectorDBManager
    │   └─→ Pinecone.query()
    │
    └─→ Returns top-k similar entries
        └─→ Based on cosine similarity
```

## Technology Stack

### Backend
- **FastAPI**: Modern web framework
- **Python 3.9+**: Programming language
- **llama-cpp-python**: LLaMA model inference
- **sentence-transformers**: Text embeddings
- **pinecone-client**: Vector database client
- **Pydantic**: Data validation
- **Uvicorn**: ASGI server

### Frontend
- **React 18**: UI framework
- **Vite**: Build tool & dev server
- **Axios**: HTTP client
- **Tailwind CSS**: Styling
- **Lucide React**: Icons

### Infrastructure
- **Pinecone**: Vector database (cloud)
- **LLaMA 2**: Language model (local)
- **Sentence Transformers**: Embedding model (local)

### DevOps (Optional)
- **Docker**: Containerization
- **Docker Compose**: Container orchestration
- **Nginx**: Reverse proxy
- **GitHub Actions**: CI/CD

## Performance Considerations

### LLM Inference
- Context window: 2048 tokens (configurable)
- Max response: 512 tokens (configurable)
- Temperature: 0.7 (configurable)
- Inference time: 2-30 seconds (depends on model size)

### Embeddings
- Vector dimension: 384 (all-MiniLM-L6-v2)
- Embedding time: <100ms per text
- Batch processing: Supported

### Vector Search
- Search time: <100ms (Pinecone cloud)
- Top-k results: Configurable (default 5)
- Namespace: "knowledge"

## Scalability

### Current Limitations
- LLM runs on single machine (CPU/GPU intensive)
- Knowledge stored in local JSON (small deployments)
- No horizontal scaling for backend

### Production Improvements
- GPU acceleration for LLM
- Database backend for knowledge (PostgreSQL + pgvector)
- Load balancing for multiple backend instances
- Caching layer (Redis)
- Message queue (Celery)

## Security

### Current Implementation
- No authentication (open API)
- CORS configured for development
- Environment variables for secrets

### Production Hardening
- API key authentication
- OAuth2/JWT tokens
- Rate limiting
- Input validation
- HTTPS/SSL
- CORS restrictions
- Database encryption
- Audit logging

## Testing

### Unit Tests
```bash
pytest backend/tests/
```

### Integration Tests
```bash
pytest backend/tests/integration/
```

### Frontend Tests
```bash
npm test
```

### API Testing
```bash
# Using examples.py
python examples.py
```

## Monitoring & Logging

### Backend Logs
- Request/response logging
- Error tracking
- Performance metrics

### Frontend Logs
- Browser console
- Network requests
- Component errors

### Health Monitoring
- `/health` endpoint
- Component availability checks
- Pinecone connectivity
- LLM responsiveness

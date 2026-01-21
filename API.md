# API Reference

## Base URL
```
http://localhost:8000
```

## Authentication
Currently, no authentication is required. For production, implement API keys or OAuth2.

## Health Check

### GET /health
Check the status of all components.

**Response:**
```json
{
  "status": "healthy",
  "llm_available": true,
  "vector_db_available": true,
  "embedding_model_available": true
}
```

## Chat Endpoints

### POST /chat
Send a user query and get a response with context from knowledge base.

**Request:**
```json
{
  "query": "How do I use Python virtual environments?",
  "conversation_history": [
    {
      "role": "user",
      "content": "What is Python?"
    },
    {
      "role": "assistant",
      "content": "Python is a programming language..."
    }
  ],
  "context_limit": 5
}
```

**Response:**
```json
{
  "response": "Virtual environments allow you to...",
  "sources": [
    {
      "id": "knowledge_1",
      "score": 0.95,
      "metadata": {
        "id": 1,
        "title": "Python Virtual Environments",
        "content": "...",
        "category": "technical"
      }
    }
  ],
  "confidence": 0.92
}
```

**Status Codes:**
- `200` - Success
- `400` - Bad request (empty query)
- `500` - Server error

## Knowledge Base Endpoints

### GET /knowledge
Get all knowledge entries.

**Response:**
```json
[
  {
    "id": 1,
    "title": "Entry Title",
    "content": "Entry content",
    "category": "general",
    "tags": ["tag1", "tag2"],
    "source": "http://source.com",
    "created_at": "2024-01-20T10:30:00",
    "updated_at": "2024-01-20T10:30:00"
  }
]
```

### POST /knowledge
Create a new knowledge entry.

**Request:**
```json
{
  "title": "Python Tips",
  "content": "Use virtual environments for project isolation",
  "category": "technical",
  "tags": ["python", "best-practices"],
  "source": "Python Official Docs"
}
```

**Response:**
```json
{
  "id": 2,
  "title": "Python Tips",
  "content": "Use virtual environments for project isolation",
  "category": "technical",
  "tags": ["python", "best-practices"],
  "source": "Python Official Docs",
  "created_at": "2024-01-20T10:35:00",
  "updated_at": "2024-01-20T10:35:00"
}
```

**Status Codes:**
- `201` - Created
- `400` - Invalid request
- `500` - Server error

### GET /knowledge/{id}
Get a specific knowledge entry.

**Parameters:**
- `id` (path) - Entry ID (integer)

**Response:**
```json
{
  "id": 1,
  "title": "Entry Title",
  "content": "Entry content",
  "category": "general",
  "tags": ["tag1"],
  "source": "source",
  "created_at": "2024-01-20T10:30:00",
  "updated_at": "2024-01-20T10:30:00"
}
```

**Status Codes:**
- `200` - Success
- `404` - Entry not found
- `500` - Server error

### PUT /knowledge/{id}
Update a knowledge entry.

**Parameters:**
- `id` (path) - Entry ID (integer)

**Request:**
```json
{
  "title": "Updated Title",
  "content": "Updated content"
}
```

**Response:** Updated entry object

**Status Codes:**
- `200` - Success
- `404` - Entry not found
- `500` - Server error

### DELETE /knowledge/{id}
Delete a knowledge entry.

**Parameters:**
- `id` (path) - Entry ID (integer)

**Response:**
```json
{
  "message": "Entry deleted successfully"
}
```

**Status Codes:**
- `200` - Success
- `404` - Entry not found
- `500` - Server error

## Search Endpoint

### POST /search
Search the knowledge base using semantic search.

**Request:**
```json
{
  "query": "Python best practices",
  "category": "technical",
  "top_k": 5
}
```

**Response:**
```json
[
  {
    "id": 1,
    "title": "Python Virtual Environments",
    "content": "Virtual environments are isolated...",
    "category": "technical",
    "tags": ["python", "best-practices"],
    "source": "Python Docs",
    "created_at": "2024-01-20T10:30:00",
    "updated_at": "2024-01-20T10:30:00"
  }
]
```

**Parameters:**
- `query` (required) - Search query string
- `category` (optional) - Filter by category
- `top_k` (optional) - Number of results (default: 5)

**Status Codes:**
- `200` - Success
- `500` - Server error

## Error Responses

All error responses follow this format:

```json
{
  "detail": "Error description"
}
```

## Rate Limiting

Not implemented by default. For production, add rate limiting using:
```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
```

## Examples

### Python
```python
import requests

BASE_URL = "http://localhost:8000"

# Chat
response = requests.post(
    f"{BASE_URL}/chat",
    json={"query": "What is Python?"}
)
print(response.json())

# Add knowledge
response = requests.post(
    f"{BASE_URL}/knowledge",
    json={
        "title": "Python Basics",
        "content": "Python is a programming language...",
        "category": "technical"
    }
)
print(response.json())
```

### JavaScript/Node.js
```javascript
const BASE_URL = "http://localhost:8000"

// Chat
const response = await fetch(`${BASE_URL}/chat`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ query: "What is Python?" })
})
console.log(await response.json())

// Add knowledge
const response = await fetch(`${BASE_URL}/knowledge`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    title: "Python Basics",
    content: "Python is a programming language...",
    category: "technical"
  })
})
console.log(await response.json())
```

### cURL
```bash
# Chat
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "What is Python?"}'

# Add knowledge
curl -X POST http://localhost:8000/knowledge \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Python Basics",
    "content": "Python is...",
    "category": "technical"
  }'
```

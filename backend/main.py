"""Main FastAPI application for personal AI assistant."""

import logging
import sys
import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from typing import List

# Add backend directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import settings
from llm_manager import LLMManager
from embedding_manager import EmbeddingManager
from vector_db import VectorDBManager
from knowledge_base import KnowledgeBase
from models import (
    ChatRequest,
    ChatResponse,
    KnowledgeEntry,
    KnowledgeRequest,
    KnowledgeUpdateRequest,
    SearchRequest,
    HealthResponse,
    Message,
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global managers
llm_manager = None
embedding_manager = None
vector_db_manager = None
knowledge_base = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events."""
    global llm_manager, embedding_manager, vector_db_manager, knowledge_base

    # Startup
    logger.info("Initializing AI Assistant components...")

    llm_manager = LLMManager(
        model_path=settings.llm_model_path,
        context_window=settings.llm_context_window,
        max_tokens=settings.llm_max_tokens,
        temperature=settings.llm_temperature,
    )

    embedding_manager = EmbeddingManager(model_name=settings.embedding_model)

    vector_db_manager = VectorDBManager(
        api_key=settings.pinecone_api_key,
        environment=settings.pinecone_environment,
        index_name=settings.pinecone_index_name,
    )

    knowledge_base = KnowledgeBase(file_path=settings.knowledge_base_path)

    logger.info("AI Assistant initialized successfully!")

    yield

    # Shutdown
    logger.info("Shutting down AI Assistant...")


# Create FastAPI app
app = FastAPI(
    title="Personal AI Assistant",
    description="A self-hosted LLM-powered assistant with vector database integration",
    version="1.0.0",
    lifespan=lifespan,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Health check endpoint
@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Check health status of all components."""
    return HealthResponse(
        status="healthy",
        llm_available=llm_manager.is_available() if llm_manager else False,
        vector_db_available=vector_db_manager.is_available() if vector_db_manager else False,
        embedding_model_available=embedding_manager.model is not None if embedding_manager else False,
    )


# Chat endpoint
@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Process user query and return assistant response.

    Uses RAG (Retrieval Augmented Generation) to provide contextual responses.
    """
    if not request.query:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Query cannot be empty")

    try:
        # Generate embedding for user query
        if not embedding_manager:
            raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Embedding service unavailable")
        query_embedding = embedding_manager.embed_text(request.query)

        # Search vector database for relevant knowledge
        if not vector_db_manager:
            sources = []
        else:
            sources = vector_db_manager.search_vectors(query_embedding=query_embedding, top_k=5)

        # Build context from retrieved sources
        context = ""
        if sources:
            context = "Relevant information:\n"
            for i, source in enumerate(sources, 1):
                metadata = source.get("metadata", {})
                context += f"{i}. {metadata.get('content', 'N/A')}\n"

        # Build system prompt
        system_prompt = (
            "You are a helpful personal AI assistant. Provide concise and accurate answers "
            "based on the provided context. If you don't know the answer, say so honestly."
        )

        # Prepare full prompt with context
        full_prompt = f"{system_prompt}\n\nContext:\n{context}\n\nUser Query: {request.query}"

        # Generate response from LLM
        if not llm_manager:
            raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="LLM service unavailable")
        response_text = llm_manager.generate(prompt=full_prompt, system_prompt=None)

        # Calculate confidence based on source similarity scores
        confidence = sum(s.get("score", 0) for s in sources) / len(sources) if sources else 0.5

        return ChatResponse(
            response=response_text,
            sources=sources,
            confidence=confidence,
        )

    except Exception as e:
        logger.error(f"Error in chat endpoint: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


# Knowledge base endpoints
@app.post("/knowledge", response_model=KnowledgeEntry)
async def add_knowledge(request: KnowledgeRequest):
    """Add a new knowledge entry."""
    try:
        # Add to local knowledge base
        if not knowledge_base:
            raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Knowledge base service unavailable")
        entry = knowledge_base.add_entry(
            title=request.title,
            content=request.content,
            category=request.category or "general",
            tags=request.tags,
            source=request.source,
        )

        # Generate embedding and add to vector database
        if embedding_manager and vector_db_manager:
            embedding = embedding_manager.embed_text(request.content)
            vector_id = f"knowledge_{entry['id']}"
            vector_db_manager.upsert_vectors(
            [(
                vector_id,
                embedding,
                {
                    "id": entry["id"],
                    "title": request.title,
                    "content": request.content,
                    "category": request.category,
                },
            )],
            namespace="knowledge",
        )

        return KnowledgeEntry(**entry)

    except Exception as e:
        logger.error(f"Error adding knowledge: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@app.get("/knowledge", response_model=List[KnowledgeEntry])
async def get_all_knowledge():
    """Get all knowledge entries."""
    try:
        if not knowledge_base:
            raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Knowledge base service unavailable")
        entries = knowledge_base.get_all_entries()
        return [KnowledgeEntry(**entry) for entry in entries]
    except Exception as e:
        logger.error(f"Error retrieving knowledge: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@app.get("/knowledge/{entry_id}", response_model=KnowledgeEntry)
async def get_knowledge(entry_id: int):
    """Get a specific knowledge entry."""
    try:
        if not knowledge_base:
            raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Knowledge base service unavailable")
        entry = knowledge_base.get_entry(entry_id)
        if not entry:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Entry not found")
        return KnowledgeEntry(**entry)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving knowledge: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@app.put("/knowledge/{entry_id}", response_model=KnowledgeEntry)
async def update_knowledge(entry_id: int, request: KnowledgeUpdateRequest):
    """Update a knowledge entry."""
    try:
        if not knowledge_base:
            raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Knowledge base service unavailable")
        update_data = request.model_dump(exclude_unset=True)
        entry = knowledge_base.update_entry(entry_id, **update_data)

        if not entry:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Entry not found")

        # Update vector database if content changed
        if "content" in update_data and embedding_manager and vector_db_manager:
            embedding = embedding_manager.embed_text(update_data["content"])
            vector_id = f"knowledge_{entry_id}"
            vector_db_manager.upsert_vectors(
                [(
                    vector_id,
                    embedding,
                    {
                        "id": entry_id,
                        "title": entry.get("title", ""),
                        "content": update_data["content"],
                        "category": entry.get("category", ""),
                    },
                )],
                namespace="knowledge",
            )

        return KnowledgeEntry(**entry)

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating knowledge: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@app.delete("/knowledge/{entry_id}")
async def delete_knowledge(entry_id: int):
    """Delete a knowledge entry."""
    try:
        if not knowledge_base:
            raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Knowledge base service unavailable")
        success = knowledge_base.delete_entry(entry_id)
        if not success:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Entry not found")

        # Delete from vector database
        if vector_db_manager:
            vector_db_manager.delete_vectors([f"knowledge_{entry_id}"], namespace="knowledge")

        return {"message": "Entry deleted successfully"}

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting knowledge: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@app.post("/search", response_model=List[KnowledgeEntry])
async def search_knowledge(request: SearchRequest):
    """Search knowledge base."""
    try:
        # Generate embedding for search query
        if not embedding_manager or not vector_db_manager or not knowledge_base:
            raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Search service unavailable")
        query_embedding = embedding_manager.embed_text(request.query)

        # Search vector database
        results = vector_db_manager.search_vectors(
            query_embedding=query_embedding,
            top_k=request.top_k if request.top_k else 5,
            namespace="knowledge",
        )

        # Extract entry IDs and fetch full entries
        entries = []
        for result in results:
            entry_id = result.get("metadata", {}).get("id")
            if entry_id:
                entry = knowledge_base.get_entry(entry_id)
                if entry:
                    entries.append(KnowledgeEntry(**entry))

        return entries

    except Exception as e:
        logger.error(f"Error searching knowledge: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app,
        host=settings.api_host,
        port=settings.api_port,
    )

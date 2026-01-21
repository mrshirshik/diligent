"""Pydantic models for API requests and responses."""

from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class Message(BaseModel):
    """Chat message model."""

    role: str = Field(..., description="Role: 'user' or 'assistant'")
    content: str = Field(..., description="Message content")
    timestamp: Optional[datetime] = None


class ChatRequest(BaseModel):
    """Chat request model."""

    query: str = Field(..., description="User query")
    conversation_history: Optional[List[Message]] = Field(default=[], description="Previous messages")
    context_limit: Optional[int] = Field(default=5, description="Number of context messages to use")


class ChatResponse(BaseModel):
    """Chat response model."""

    response: str = Field(..., description="Assistant response")
    sources: Optional[List[dict]] = Field(default=[], description="Retrieved knowledge sources")
    confidence: Optional[float] = Field(default=0.0, description="Response confidence score")


class KnowledgeEntry(BaseModel):
    """Knowledge base entry model."""

    id: Optional[int] = None
    title: str = Field(..., description="Entry title")
    content: str = Field(..., description="Entry content")
    category: str = Field(default="general", description="Entry category")
    tags: Optional[List[str]] = Field(default=[], description="Entry tags")
    source: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class KnowledgeRequest(BaseModel):
    """Request to add/update knowledge."""

    title: str = Field(..., description="Entry title")
    content: str = Field(..., description="Entry content")
    category: str = Field(default="general", description="Entry category")
    tags: Optional[List[str]] = Field(default=[], description="Entry tags")
    source: Optional[str] = None


class KnowledgeUpdateRequest(BaseModel):
    """Request to update knowledge entry."""

    title: Optional[str] = None
    content: Optional[str] = None
    category: Optional[str] = None
    tags: Optional[List[str]] = None
    source: Optional[str] = None


class SearchRequest(BaseModel):
    """Knowledge search request."""

    query: str = Field(..., description="Search query")
    category: Optional[str] = None
    top_k: int = Field(default=5, description="Number of results to return")


class HealthResponse(BaseModel):
    """Health check response."""

    status: str
    llm_available: bool
    vector_db_available: bool
    embedding_model_available: bool

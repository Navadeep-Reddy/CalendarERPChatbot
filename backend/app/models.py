"""
Pydantic models for request/response validation
"""
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class ChatRequest(BaseModel):
    """Request model for chat queries"""
    query: str = Field(..., description="User's question about the calendar")
    session_id: Optional[str] = Field(None, description="Optional session ID for conversation context")
    
    class Config:
        json_schema_extra = {
            "example": {
                "query": "When is the mid-term exam scheduled?",
                "session_id": "user123"
            }
        }


class SourceDocument(BaseModel):
    """Model for source documents used in RAG"""
    content: str = Field(..., description="Content of the source document")
    metadata: dict = Field(default_factory=dict, description="Metadata about the source")


class ChatResponse(BaseModel):
    """Response model for chat queries"""
    answer: str = Field(..., description="Generated answer from the chatbot")
    sources: List[SourceDocument] = Field(default_factory=list, description="Source documents used")
    session_id: Optional[str] = Field(None, description="Session ID")
    
    class Config:
        json_schema_extra = {
            "example": {
                "answer": "The mid-term examinations are scheduled from March 15-20, 2024.",
                "sources": [
                    {
                        "content": "Mid-term examinations: March 15-20, 2024",
                        "metadata": {"event_type": "examination", "semester": "Spring 2024"}
                    }
                ],
                "session_id": "user123"
            }
        }


class CalendarEvent(BaseModel):
    """Model for calendar events"""
    event_id: str = Field(..., description="Unique identifier for the event")
    title: str = Field(..., description="Event title")
    description: Optional[str] = Field(None, description="Detailed description")
    start_date: str = Field(..., description="Start date of the event")
    end_date: Optional[str] = Field(None, description="End date (for multi-day events)")
    event_type: str = Field(..., description="Type of event (exam, holiday, etc.)")
    semester: Optional[str] = Field(None, description="Academic semester")
    year: str = Field(..., description="Academic year")
    
    class Config:
        json_schema_extra = {
            "example": {
                "event_id": "evt_001",
                "title": "Mid-term Examinations",
                "description": "Mid-semester examinations for all courses",
                "start_date": "2024-03-15",
                "end_date": "2024-03-20",
                "event_type": "examination",
                "semester": "Spring",
                "year": "2023-2024"
            }
        }


class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    version: str
    timestamp: str

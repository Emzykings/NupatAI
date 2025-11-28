"""
Chat schemas for request/response validation
"""
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
import uuid


class ChatCreate(BaseModel):
    """Schema for creating a new chat"""
    title: Optional[str] = Field(default="New Chat", description="Chat title (optional)")


class ChatUpdate(BaseModel):
    """Schema for updating chat title"""
    title: str = Field(..., min_length=1, max_length=200, description="New chat title")


class ChatResponse(BaseModel):
    """Schema for chat data in responses"""
    id: uuid.UUID
    user_id: uuid.UUID
    title: str
    message_count: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class ChatListResponse(BaseModel):
    """Schema for paginated chat list"""
    chats: List[ChatResponse]
    total: int
    page: int
    page_size: int
    total_pages: int


class ChatDeleteResponse(BaseModel):
    """Schema for chat deletion response"""
    message: str = "Chat deleted successfully"
    chat_id: uuid.UUID
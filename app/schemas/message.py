"""
Message schemas for request/response validation
"""
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
import uuid
from app.db.models import MessageRole


class MessageCreate(BaseModel):
    """Schema for creating a new message (user sends message)"""
    content: str = Field(..., min_length=1, description="Message content")


class MessageResponse(BaseModel):
    """Schema for message data in responses"""
    id: uuid.UUID
    chat_id: uuid.UUID
    role: MessageRole
    content: str
    created_at: datetime
    
    class Config:
        from_attributes = True


class MessageListResponse(BaseModel):
    """Schema for paginated message list"""
    messages: List[MessageResponse]
    total: int
    page: int
    page_size: int
    total_pages: int


class ChatWithMessages(BaseModel):
    """Schema for chat with all its messages"""
    id: uuid.UUID
    user_id: uuid.UUID
    title: str
    message_count: int
    created_at: datetime
    updated_at: datetime
    messages: List[MessageResponse]
    
    class Config:
        from_attributes = True


class MessageSendResponse(BaseModel):
    """Schema for response after sending a message"""
    user_message: MessageResponse
    assistant_message: MessageResponse
    chat: dict  # Updated chat info (title may have changed)
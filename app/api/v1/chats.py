"""
Chat API endpoints
Handles chat CRUD operations
"""
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from typing import List
import uuid
import math
from app.db.session import get_db
from app.db.models import User
from app.schemas.chat import (
    ChatCreate,
    ChatUpdate,
    ChatResponse,
    ChatListResponse,
    ChatDeleteResponse
)
from app.schemas.message import ChatWithMessages
from app.services.chat_service import ChatService
from app.api.deps import get_current_user


router = APIRouter(prefix="/chats", tags=["Chats"])


@router.post("", response_model=ChatResponse, status_code=status.HTTP_201_CREATED)
def create_chat(
    chat_data: ChatCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create a new chat
    
    - **title**: Optional chat title (defaults to "New Chat")
    
    The chat title will be automatically updated when the first message is sent.
    
    Requires: Bearer token in Authorization header
    """
    chat = ChatService.create_chat(db, current_user, chat_data)
    return ChatResponse.model_validate(chat)


@router.get("", response_model=ChatListResponse)
def get_user_chats(
    page: int = Query(1, ge=1, description="Page number (starts at 1)"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page (max 100)"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get all chats for the current user (paginated)
    
    - **page**: Page number (default: 1)
    - **page_size**: Number of chats per page (default: 20, max: 100)
    
    Returns chats ordered by most recent activity first.
    
    Requires: Bearer token in Authorization header
    """
    chats, total = ChatService.get_user_chats(db, current_user, page, page_size)
    
    total_pages = math.ceil(total / page_size) if total > 0 else 0
    
    return ChatListResponse(
        chats=[ChatResponse.model_validate(chat) for chat in chats],
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages
    )


@router.get("/{chat_id}", response_model=ChatWithMessages)
def get_chat_with_messages(
    chat_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get a specific chat with all its messages
    
    - **chat_id**: UUID of the chat
    
    Returns chat details and all messages in chronological order.
    
    Requires: Bearer token in Authorization header
    """
    chat = ChatService.get_chat_by_id(db, chat_id, current_user)
    return ChatWithMessages.model_validate(chat)


@router.patch("/{chat_id}", response_model=ChatResponse)
def update_chat_title(
    chat_id: uuid.UUID,
    update_data: ChatUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update chat title
    
    - **chat_id**: UUID of the chat
    - **title**: New chat title (1-200 characters)
    
    Requires: Bearer token in Authorization header
    """
    chat = ChatService.update_chat_title(db, chat_id, current_user, update_data)
    return ChatResponse.model_validate(chat)


@router.delete("/{chat_id}", response_model=ChatDeleteResponse)
def delete_chat(
    chat_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Delete a chat and all its messages
    
    - **chat_id**: UUID of the chat
    
    This action cannot be undone. All messages in the chat will be permanently deleted.
    
    Requires: Bearer token in Authorization header
    """
    ChatService.delete_chat(db, chat_id, current_user)
    return ChatDeleteResponse(
        message="Chat deleted successfully",
        chat_id=chat_id
    )
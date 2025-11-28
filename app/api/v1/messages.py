"""
Message API endpoints
Handles sending messages and getting chat messages
"""
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
import uuid
import math
from app.db.session import get_db
from app.db.models import User
from app.schemas.message import (
    MessageCreate,
    MessageResponse,
    MessageListResponse,
    MessageSendResponse
)
from app.schemas.chat import ChatResponse
from app.services.chat_service import ChatService
from app.services.message_service import MessageService
from app.api.deps import get_current_user


router = APIRouter(prefix="/chats", tags=["Messages"])


@router.post("/{chat_id}/messages", response_model=MessageSendResponse, status_code=status.HTTP_201_CREATED)
def send_message(
    chat_id: uuid.UUID,
    message_data: MessageCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Send a message in a chat and receive AI response
    
    - **chat_id**: UUID of the chat
    - **content**: Message content (required)
    
    This endpoint:
    1. Saves your message
    2. Generates an AI response using NupatAI
    3. Saves the AI response
    4. Auto-generates chat title if this is the first message
    5. Returns both messages and updated chat info
    
    Requires: Bearer token in Authorization header
    """
    # Verify chat belongs to user
    chat = ChatService.get_chat_by_id(db, chat_id, current_user)
    
    # Create message and get AI response
    user_message, assistant_message, title_generated = MessageService.create_message_and_respond(
        db, chat, message_data
    )
    
    return MessageSendResponse(
        user_message=MessageResponse.model_validate(user_message),
        assistant_message=MessageResponse.model_validate(assistant_message),
        chat={
            "id": str(chat.id),
            "title": chat.title,
            "message_count": chat.message_count,
            "title_generated": title_generated
        }
    )


@router.get("/{chat_id}/messages", response_model=MessageListResponse)
def get_chat_messages(
    chat_id: uuid.UUID,
    page: int = Query(1, ge=1, description="Page number (starts at 1)"),
    page_size: int = Query(50, ge=1, le=100, description="Items per page (max 100)"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get all messages in a chat (paginated)
    
    - **chat_id**: UUID of the chat
    - **page**: Page number (default: 1)
    - **page_size**: Number of messages per page (default: 50, max: 100)
    
    Returns messages in chronological order (oldest first).
    
    Requires: Bearer token in Authorization header
    """
    # Verify chat belongs to user
    chat = ChatService.get_chat_by_id(db, chat_id, current_user)
    
    # Get paginated messages
    messages, total = MessageService.get_chat_messages(db, chat, page, page_size)
    
    total_pages = math.ceil(total / page_size) if total > 0 else 0
    
    return MessageListResponse(
        messages=[MessageResponse.model_validate(msg) for msg in messages],
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages
    )
"""
Message service
Handles message operations and AI response generation
"""
from sqlalchemy.orm import Session
from typing import List, Tuple
from app.db.models import Message, Chat, User, MessageRole
from app.schemas.message import MessageCreate
from app.services.ai_service import ai_service
import uuid


class MessageService:
    """Service for handling message operations"""
    
    @staticmethod
    def get_chat_messages(
        db: Session,
        chat: Chat,
        page: int = 1,
        page_size: int = 50
    ) -> Tuple[List[Message], int]:
        """
        Get paginated messages for a chat
        
        Args:
            db: Database session
            chat: Chat object
            page: Page number (starts at 1)
            page_size: Number of messages per page
            
        Returns:
            Tuple[List[Message], int]: List of messages and total count
        """
        # Get total count
        total = db.query(Message).filter(Message.chat_id == chat.id).count()
        
        # Get paginated messages (ordered by creation time)
        offset = (page - 1) * page_size
        messages = (
            db.query(Message)
            .filter(Message.chat_id == chat.id)
            .order_by(Message.created_at.asc())
            .offset(offset)
            .limit(page_size)
            .all()
        )
        
        return messages, total
    
    @staticmethod
    def create_message_and_respond(
        db: Session,
        chat: Chat,
        message_data: MessageCreate
    ) -> Tuple[Message, Message, bool]:
        """
        Create user message and generate AI response
        
        Args:
            db: Database session
            chat: Chat object
            message_data: Message creation data
            
        Returns:
            Tuple[Message, Message, bool]: User message, AI message, and whether title was generated
        """
        # Get existing messages for context
        existing_messages = (
            db.query(Message)
            .filter(Message.chat_id == chat.id)
            .order_by(Message.created_at.asc())
            .all()
        )
        
        is_first_message = len(existing_messages) == 0
        
        # Create user message
        user_message = Message(
            chat_id=chat.id,
            role=MessageRole.USER,
            content=message_data.content
        )
        db.add(user_message)
        db.flush()  # Flush to get the ID without committing
        
        # Generate AI response
        ai_response_text = ai_service.generate_response(
            user_message=message_data.content,
            chat_history=existing_messages
        )
        
        # Create assistant message
        assistant_message = Message(
            chat_id=chat.id,
            role=MessageRole.ASSISTANT,
            content=ai_response_text
        )
        db.add(assistant_message)
        
        # Update chat message count
        chat.message_count = len(existing_messages) + 2  # +2 for user and assistant messages
        
        # Generate chat title if this is the first message
        title_generated = False
        if is_first_message:
            new_title = ai_service.generate_chat_title(message_data.content)
            if new_title and new_title != "New Chat":
                chat.title = new_title
                title_generated = True
        
        # Commit all changes
        db.commit()
        db.refresh(user_message)
        db.refresh(assistant_message)
        db.refresh(chat)
        
        return user_message, assistant_message, title_generated
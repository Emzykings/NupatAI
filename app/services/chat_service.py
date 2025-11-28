"""
Chat service
Handles chat CRUD operations
"""
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import List, Tuple
from app.db.models import Chat, User
from app.schemas.chat import ChatCreate, ChatUpdate
import uuid
import math


class ChatService:
    """Service for handling chat operations"""
    
    @staticmethod
    def create_chat(db: Session, user: User, chat_data: ChatCreate) -> Chat:
        """
        Create a new chat for user
        
        Args:
            db: Database session
            user: User object
            chat_data: Chat creation data
            
        Returns:
            Chat: Created chat object
        """
        new_chat = Chat(
            user_id=user.id,
            title=chat_data.title or "New Chat"
        )
        
        db.add(new_chat)
        db.commit()
        db.refresh(new_chat)
        
        return new_chat
    
    @staticmethod
    def get_user_chats(
        db: Session, 
        user: User, 
        page: int = 1, 
        page_size: int = 20
    ) -> Tuple[List[Chat], int]:
        """
        Get paginated list of user's chats
        
        Args:
            db: Database session
            user: User object
            page: Page number (starts at 1)
            page_size: Number of chats per page
            
        Returns:
            Tuple[List[Chat], int]: List of chats and total count
        """
        # Get total count
        total = db.query(Chat).filter(Chat.user_id == user.id).count()
        
        # Get paginated chats (ordered by most recent first)
        offset = (page - 1) * page_size
        chats = (
            db.query(Chat)
            .filter(Chat.user_id == user.id)
            .order_by(Chat.updated_at.desc())
            .offset(offset)
            .limit(page_size)
            .all()
        )
        
        return chats, total
    
    @staticmethod
    def get_chat_by_id(db: Session, chat_id: uuid.UUID, user: User) -> Chat:
        """
        Get a specific chat by ID
        
        Args:
            db: Database session
            chat_id: Chat UUID
            user: User object
            
        Returns:
            Chat: Chat object
            
        Raises:
            HTTPException: If chat not found or doesn't belong to user
        """
        chat = db.query(Chat).filter(Chat.id == chat_id).first()
        
        if not chat:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Chat not found"
            )
        
        # Verify chat belongs to user
        if chat.user_id != user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to access this chat"
            )
        
        return chat
    
    @staticmethod
    def update_chat_title(
        db: Session, 
        chat_id: uuid.UUID, 
        user: User, 
        update_data: ChatUpdate
    ) -> Chat:
        """
        Update chat title
        
        Args:
            db: Database session
            chat_id: Chat UUID
            user: User object
            update_data: Chat update data
            
        Returns:
            Chat: Updated chat object
        """
        chat = ChatService.get_chat_by_id(db, chat_id, user)
        
        chat.title = update_data.title
        db.commit()
        db.refresh(chat)
        
        return chat
    
    @staticmethod
    def delete_chat(db: Session, chat_id: uuid.UUID, user: User) -> None:
        """
        Delete a chat (and all its messages via cascade)
        
        Args:
            db: Database session
            chat_id: Chat UUID
            user: User object
        """
        chat = ChatService.get_chat_by_id(db, chat_id, user)
        
        db.delete(chat)
        db.commit()
    
    @staticmethod
    def update_chat_message_count(db: Session, chat: Chat) -> None:
        """
        Update the message count for a chat
        
        Args:
            db: Database session
            chat: Chat object
        """
        chat.message_count = len(chat.messages)
        db.commit()
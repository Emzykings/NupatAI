"""
AI service
Handles integration with Groq API for fast, reliable AI responses
"""
from groq import Groq
from fastapi import HTTPException, status
from typing import List
from app.core.config import settings
from app.core.prompts import get_system_prompt, get_title_generation_prompt, format_chat_history
from app.db.models import Message


class AIService:
    """Service for handling AI interactions with Groq"""
    
    def __init__(self):
        """Initialize AI service with Groq client"""
        self.client = Groq(api_key=settings.GROQ_API_KEY)
        self.model = settings.GROQ_MODEL
    
    def generate_response(self, user_message: str, chat_history: List[Message] = None) -> str:
        """
        Generate AI response to user message using Groq
        
        Args:
            user_message: User's message
            chat_history: Previous messages in the chat (optional)
            
        Returns:
            str: AI-generated response
            
        Raises:
            HTTPException: If AI generation fails
        """
        try:
            # Build messages for Groq chat completion
            messages = [
                {
                    "role": "system",
                    "content": get_system_prompt()
                }
            ]
            
            # Add chat history for context (last 10 messages)
            if chat_history:
                recent_messages = chat_history[-10:] if len(chat_history) > 10 else chat_history
                for msg in recent_messages:
                    messages.append({
                        "role": "user" if msg.role == "user" else "assistant",
                        "content": msg.content
                    })
            
            # Add current user message
            messages.append({
                "role": "user",
                "content": user_message
            })
            
            # Generate response with Groq
            chat_completion = self.client.chat.completions.create(
                messages=messages,
                model=self.model,
                temperature=0.7,
                max_tokens=2048,
                top_p=0.95,
            )
            
            response_text = chat_completion.choices[0].message.content
            
            if not response_text:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Failed to generate AI response"
                )
            
            return response_text.strip()
            
        except Exception as e:
            print(f"AI generation error: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"AI service error: {str(e)}"
            )
    
    def generate_chat_title(self, first_message: str) -> str:
        """
        Generate a title for the chat based on the first message
        
        Args:
            first_message: The user's first message in the chat
            
        Returns:
            str: Generated chat title (3-6 words)
        """
        try:
            messages = [
                {
                    "role": "system",
                    "content": "You are a helpful assistant that creates short, concise chat titles."
                },
                {
                    "role": "user",
                    "content": get_title_generation_prompt(first_message)
                }
            ]
            
            chat_completion = self.client.chat.completions.create(
                messages=messages,
                model=self.model,
                temperature=0.5,
                max_tokens=20,
            )
            
            title = chat_completion.choices[0].message.content.strip()
            
            # Clean and validate title
            if not title:
                return "New Chat"
            
            # Remove quotes if present
            title = title.strip('"\'')
            
            # Ensure title is not too long
            words = title.split()
            if len(words) > 6:
                title = " ".join(words[:6])
            
            # Limit length to 200 characters (database constraint)
            if len(title) > 200:
                title = title[:197] + "..."
            
            return title
            
        except Exception as e:
            print(f"Title generation error: {str(e)}")
            # Return default title if generation fails
            return "New Chat"


# Create singleton instance
ai_service = AIService()
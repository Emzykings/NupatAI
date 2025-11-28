"""
Authentication schemas for request/response validation
"""
from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional
from datetime import datetime
import uuid


class UserSignup(BaseModel):
    """Schema for user signup request"""
    email: EmailStr = Field(..., description="User email address")
    phone: Optional[str] = Field(None, description="User phone number (optional)")
    password: str = Field(..., min_length=8, description="User password (min 8 characters)")
    
    @validator('phone')
    def validate_phone(cls, v):
        """Validate phone number format"""
        if v is not None and v.strip():
            # Remove spaces and check if it contains only digits and + -
            cleaned = v.replace(" ", "").replace("-", "")
            if not cleaned.replace("+", "").isdigit():
                raise ValueError("Phone number must contain only digits, spaces, hyphens, and optional + prefix")
            if len(cleaned) < 10:
                raise ValueError("Phone number must be at least 10 digits")
        return v


class UserLogin(BaseModel):
    """Schema for user login request"""
    email: EmailStr = Field(..., description="User email address")
    password: str = Field(..., description="User password")


class Token(BaseModel):
    """Schema for authentication token response"""
    access_token: str = Field(..., description="JWT access token")
    token_type: str = Field(default="bearer", description="Token type")


class TokenData(BaseModel):
    """Schema for decoded token data"""
    user_id: uuid.UUID
    email: str


class UserResponse(BaseModel):
    """Schema for user data in responses"""
    id: uuid.UUID
    email: str
    phone: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True


class LoginResponse(BaseModel):
    """Schema for complete login response"""
    access_token: str
    token_type: str = "bearer"
    user: UserResponse


class LogoutResponse(BaseModel):
    """Schema for logout response"""
    message: str = "Successfully logged out"
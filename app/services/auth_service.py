"""
Authentication service
Handles user registration, login, and authentication logic
"""
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.db.models import User
from app.core.security import get_password_hash, verify_password, create_access_token
from app.schemas.auth import UserSignup, UserLogin


class AuthService:
    """Service for handling authentication operations"""
    
    @staticmethod
    def create_user(db: Session, user_data: UserSignup) -> User:
        """
        Create a new user
        
        Args:
            db: Database session
            user_data: User signup data
            
        Returns:
            User: Created user object
            
        Raises:
            HTTPException: If email or phone already exists
        """
        # Check if email already exists
        existing_user = db.query(User).filter(User.email == user_data.email).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # Check if phone already exists (if provided)
        if user_data.phone:
            existing_phone = db.query(User).filter(User.phone == user_data.phone).first()
            if existing_phone:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Phone number already registered"
                )
        
        # Create new user
        hashed_password = get_password_hash(user_data.password)
        new_user = User(
            email=user_data.email,
            phone=user_data.phone,
            hashed_password=hashed_password
        )
        
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
        return new_user
    
    @staticmethod
    def authenticate_user(db: Session, login_data: UserLogin) -> User:
        """
        Authenticate a user with email and password
        
        Args:
            db: Database session
            login_data: User login credentials
            
        Returns:
            User: Authenticated user object
            
        Raises:
            HTTPException: If credentials are invalid
        """
        user = db.query(User).filter(User.email == login_data.email).first()
        
        if not user or not verify_password(login_data.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"}
            )
        
        return user
    
    @staticmethod
    def create_user_token(user: User) -> str:
        """
        Create access token for user
        
        Args:
            user: User object
            
        Returns:
            str: JWT access token
        """
        token_data = {
            "sub": str(user.id),
            "email": user.email
        }
        return create_access_token(token_data)
    
    @staticmethod
    def get_user_by_id(db: Session, user_id: str) -> User:
        """
        Get user by ID
        
        Args:
            db: Database session
            user_id: User UUID
            
        Returns:
            User: User object
            
        Raises:
            HTTPException: If user not found
        """
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        return user
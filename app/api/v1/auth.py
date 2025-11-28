"""
Authentication API endpoints
Handles user signup, login, logout, and user info
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models import User
from app.schemas.auth import (
    UserSignup, 
    UserLogin, 
    LoginResponse, 
    LogoutResponse, 
    UserResponse
)
from app.services.auth_service import AuthService
from app.api.deps import get_current_user


router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/signup", response_model=LoginResponse, status_code=status.HTTP_201_CREATED)
def signup(
    user_data: UserSignup,
    db: Session = Depends(get_db)
):
    """
    Register a new user
    
    - **email**: Valid email address (required)
    - **phone**: Phone number (optional)
    - **password**: Minimum 8 characters (required)
    
    Returns access token and user information
    """
    # Create user
    user = AuthService.create_user(db, user_data)
    
    # Generate access token
    access_token = AuthService.create_user_token(user)
    
    return LoginResponse(
        access_token=access_token,
        token_type="bearer",
        user=UserResponse.model_validate(user)
    )


@router.post("/login", response_model=LoginResponse)
def login(
    login_data: UserLogin,
    db: Session = Depends(get_db)
):
    """
    Login with email and password
    
    - **email**: User's email address
    - **password**: User's password
    
    Returns access token and user information
    """
    # Authenticate user
    user = AuthService.authenticate_user(db, login_data)
    
    # Generate access token
    access_token = AuthService.create_user_token(user)
    
    return LoginResponse(
        access_token=access_token,
        token_type="bearer",
        user=UserResponse.model_validate(user)
    )


@router.post("/logout", response_model=LogoutResponse)
def logout(current_user: User = Depends(get_current_user)):
    """
    Logout current user
    
    Note: With JWT tokens, logout is handled client-side by removing the token.
    This endpoint confirms successful logout.
    
    Requires: Bearer token in Authorization header
    """
    return LogoutResponse(message="Successfully logged out")


@router.get("/me", response_model=UserResponse)
def get_current_user_info(current_user: User = Depends(get_current_user)):
    """
    Get current authenticated user's information
    
    Requires: Bearer token in Authorization header
    
    Returns user profile data
    """
    return UserResponse.model_validate(current_user)
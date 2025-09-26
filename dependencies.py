from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from database.database import get_db
from models.user import User
# import jwt
from typing import Optional
from fastapi import Path
from models.merchant_token import MerchantToken 

def get_clover_token(
    merchant_id: str = Path(...),
    db: Session = Depends(get_db)
) -> str:
    """
    Dependency to fetch the latest Clover access token for a merchant from the database.
    """
    # Note: The logic in test2/items.py is slightly different and better
    # than this original dependency. We will rely on the logic inside the route itself,
    # but this function is still required for the dependency injection to work.
    
    # We'll use the logic from the original test2 dependency file.
    token_record = db.query(MerchantToken).filter(
        MerchantToken.merchant_id == merchant_id  # This assumes your MerchantToken model has merchant_id
    ).order_by(MerchantToken.created_at.desc()).first()

    if not token_record or not token_record.token:
        raise HTTPException(
            status_code=404,
            detail=f"No valid Clover API token found for merchant ID: {merchant_id}"
        )
    return token_record.token



# Security scheme for JWT tokens
security = HTTPBearer()

# Secret key for JWT - In production, use environment variables
SECRET_KEY = "your-secret-key-here"  # Change this to a secure random key
ALGORITHM = "HS256"

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """
    Dependency to get the current authenticated user from JWT token
    """
    try:
        # Extract token from credentials
        token = credentials.credentials

        # Decode JWT token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("sub")

        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )

    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Get user from database
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user

def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    """
    Dependency to get the current active user (if you have user status tracking)
    """
    if not getattr(current_user, 'is_active', True):
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

# Optional: Simple version without JWT (for development/testing)
def get_current_user_simple(db: Session = Depends(get_db)) -> User:
    """
    Simplified version that returns the first user (for development only)
    Remove this in production!
    """
    user = db.query(User).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No user found"
        )
    return user

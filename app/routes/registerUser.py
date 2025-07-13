"""
users.py (User Registration)

This module provides user-related endpoints including registration.

Routes:
- POST /users — Register a new user

Details:
- Uses bcrypt for password hashing.
- Ensures unique usernames before creating a user.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import User
from ..schemas import registrationResponse, userMetadata

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    summary="Creates, registers a user",
    description="Creates a User in the datase with necessary hashing",
    response_model=registrationResponse,
)
def createUser(
    user: userMetadata,
    db: Session = Depends(get_db),
):
    """
    Registers a new user in the system.

    Args:
        user (userMetadata): Pydantic model containing username, email, gender, and password.
        db (Session): SQLAlchemy database session.

    Returns:
        registrationResponse: Contains the registered user's public information.

    Raises:
        HTTPException:
            - 400 if a user with the given username already exists.
    """
    existingUsers = (
        db.query(User.username).filter(User.username == user.username).first()
    )
    if existingUsers:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already exists",
        )

    new_user = User(
        username=user.username,
        email=user.email,
        gender=user.gender,
        password=pwd_context.hash(user.password),
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

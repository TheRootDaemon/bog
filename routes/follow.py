"""
users.py

This module provides endpoints for user interactions such as following and unfollowing other users.

Routes:
- POST /users/{user_id}/follow — Follow a user
- DELETE /users/{user_id}/unfollow — Unfollow a user

Authentication:
- Both routes require a valid JWT token to identify the current user.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import User
from .auth import get_current_user

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.post("/{user_id}/follow", summary="Follows a User")
def follow(
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Allows the current user to follow another user by user_id.

    Args:
        user_id (int): ID of the user to follow.
        current_user (User): The authenticated user performing the follow.
        db (Session): SQLAlchemy database session.

    Returns:
        dict: Message indicating success and updated follower/following counts.

    Raises:
        HTTPException:
            - 404 if the target user doesn't exist.
            - 400 if the user tries to follow themselves or already follows the user.
    """
    user_to_follow = db.query(User).filter(User.id == user_id).first()

    if not user_to_follow:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    if current_user == user_to_follow:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="You cannot follow yourself"
        )

    if user_to_follow in current_user.following:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You are already following the user",
        )

    current_user.following.append(user_to_follow)
    db.commit()

    return {
        "message": f"You are now following {user_to_follow.username}",
        "following_count": len(current_user.following),
        "followers_count": len(current_user.followers),
    }


@router.delete("/{user_id}/unfollow", summary="Unfollows a user")
def unfollow(
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Allows the current user to unfollow another user by user_id.

    Args:
        user_id (int): ID of the user to unfollow.
        current_user (User): The authenticated user performing the unfollow.
        db (Session): SQLAlchemy database session.

    Returns:
        dict: Message indicating success and updated follower/following counts.

    Raises:
        HTTPException:
            - 404 if the target user doesn't exist.
            - 400 if the user tries to unfollow themselves or someone they don’t follow.
    """
    user_to_unfollow = db.query(User).filter(User.id == user_id).first()

    if not user_to_unfollow:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    if current_user == user_to_unfollow:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You cannot unfollow yourself",
        )

    if user_to_unfollow not in current_user.following:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You are not following the user",
        )

    current_user.following.remove(user_to_unfollow)
    db.commit()

    return {
        "message": f"You are now not following {user_to_unfollow.username}",
        "following_count": len(current_user.following),
        "followers_count": len(current_user.followers),
    }

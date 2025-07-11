"""
feed.py

This module provides feed-related endpoints for the application,
including fetching random users and retrieving posts for a specific user.

Endpoints:
- GET /feed/getUsers: Returns a list of random users for the feed.
- GET /feed/getPosts/{username}: Returns all posts made by a given user.
"""

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import func

from ..database import get_db
from ..models import Post, User
from ..schemas import userSummary

router = APIRouter(
    prefix="/feed",
    tags=["Feed"],
)


@router.get(
    "/getUsers",
    summary="Fetches users for the Feed",
    description="Fetches random users for the sake of the feed",
    response_model=List[userSummary],
)
def getUsers(db: Session = Depends(get_db)):
    """
    Fetches a random set of 5 users from the database to populate the feed.

    Returns:
        List[userSummary]: A list of user summaries including id, username, gender, and follower count.

    Notes:
        - If there are fewer than 5 users in the database, it returns all available users.
    """
    users = db.query(User).order_by(func.random()).limit(5).all()
    result = [
        userSummary(
            id=user.id,  # type:ignore
            username=user.username,  # type:ignore
            gender=user.gender,  # type:ignore
            followersCount=len(user.followers),
        )
        for user in users
    ]

    return result


@router.get(
    "/getPosts/{username}",
    summary="Fetches posts of a certain user",
)
def getPosts(username: str, db: Session = Depends(get_db)):
    """
    Retrieves all posts made by a specific user.

    Args:
        username (str): The username whose posts should be fetched.
        db (Session): SQLAlchemy database session.

    Returns:
        List[Post]: A list of post objects authored by the user.
        OR
        Dict[str, str]: A message if no posts are found.

    Raises:
        HTTPException: 404 if the user is not found in the database.
    """
    user = db.query(User).filter(User.username == username).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    posts = db.query(Post).filter(Post.author == user.id).all()

    if not posts:
        return {"message": "The user has not posted anything yet"}

    return posts

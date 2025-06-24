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
    users = db.query(User).order_by(func.random()).limit(5).all()
    result = [
        userSummary(
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
    user = db.query(User).filter(User.username == username).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    posts = db.query(Post).filter(Post.author == user.id).all()

    if not posts:
        return {"message": "The user has not posted anything yet"}

    return posts

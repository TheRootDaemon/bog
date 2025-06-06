from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import User
from .auth import get_current_user

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.post("/follow/{user_id}")
def follow(
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    user_to_follow = db.query(User).filter(User.id == user_id).first()

    if not user_to_follow:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    if current_user == user_to_follow:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="You cannot follow yourself"
        )

    if user_to_follow == current_user.following:
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

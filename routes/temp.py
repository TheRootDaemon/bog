from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import User
from .auth import get_current_user  # Assuming you have authentication

router = APIRouter()


@router.post("/users/{user_id}/follow")
async def follow_user(
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Follow a user"""
    # Check if user to follow exists
    user_to_follow = db.query(User).filter(User.id == user_id).first()
    if not user_to_follow:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    # Check if user is trying to follow themselves
    if current_user.id == user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="You cannot follow yourself"
        )

    # Check if already following
    if user_to_follow in current_user.following:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You are already following this user",
        )

    # Add to following list
    current_user.following.append(user_to_follow)
    db.commit()

    return {
        "message": f"You are now following {user_to_follow.username}",
        "following_count": len(current_user.following),
        "followers_count": len(user_to_follow.followers),
    }


@router.delete("/users/{user_id}/follow")
async def unfollow_user(
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Unfollow a user"""
    # Check if user to unfollow exists
    user_to_unfollow = db.query(User).filter(User.id == user_id).first()
    if not user_to_unfollow:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    # Check if user is trying to unfollow themselves
    if current_user.id == user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You cannot unfollow yourself",
        )

    # Check if not following
    if user_to_unfollow not in current_user.following:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You are not following this user",
        )

    # Remove from following list
    current_user.following.remove(user_to_unfollow)
    db.commit()

    return {
        "message": f"You have unfollowed {user_to_unfollow.username}",
        "following_count": len(current_user.following),
        "followers_count": len(user_to_unfollow.followers),
    }


@router.get("/users/{user_id}/followers")
async def get_followers(user_id: int, db: Session = Depends(get_db)):
    """Get list of followers for a user"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    followers = [
        {"id": follower.id, "username": follower.username, "email": follower.email}
        for follower in user.followers
    ]

    return {
        "user_id": user_id,
        "username": user.username,
        "followers_count": len(followers),
        "followers": followers,
    }


@router.get("/users/{user_id}/following")
async def get_following(user_id: int, db: Session = Depends(get_db)):
    """Get list of users that a user is following"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    following = [
        {"id": followed.id, "username": followed.username, "email": followed.email}
        for followed in user.following
    ]

    return {
        "user_id": user_id,
        "username": user.username,
        "following_count": len(following),
        "following": following,
    }

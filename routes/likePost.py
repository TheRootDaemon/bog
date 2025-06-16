from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Post, User
from .auth import get_current_user

router = APIRouter(
    prefix="/posts",
    tags=["Posts"],
)


@router.post(
    "likePost/{post_id}",
    summary="Likes a post",
)
def likePost(
    post_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.id == current_user.id).first()
    post = db.query(Post).filter(Post.id == post_id).first()

    if not user or not post:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User or post not found",
        )

    if post in user.likedPosts:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You have already liked this post",
        )

    user.likedPosts.append(post)
    db.commit()

    return {"message": "You have liked {post.title}"}


@router.delete(
    "unlikePost/{post_id",
    summary="Unlikes a post",
)
def unlikePost(
    post_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):

    user = db.query(User).filter(User.id == current_user.id).first()
    post = db.query(Post).filter(Post.id == post_id).first()

    if not user or not post:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User or post not found",
        )

    if post not in user.likedPosts:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You have to like the post to unlike a post",
        )

    user.likedPosts.remove(post)
    db.commit()

    return {"message": f"You have unliked {post.title}"}

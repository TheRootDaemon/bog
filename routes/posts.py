from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import delete
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Post, User
from ..schemas import postMetadata, postResponse
from .auth import get_current_user

router = APIRouter(
    prefix="/posts",
    tags=["Posts"],
)


@router.post("createPost", response_model=postResponse)
def createPost(
    postData: postMetadata,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    post = Post(author=current_user.id, title=postData.title, content=postData.content)

    db.add(post)
    db.commit()
    db.refresh(post)

    return post


@router.delete("deletePost/{post_id}")
def deletePost(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    post = db.query(Post).filter(Post.id == post_id).first()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not Found"
        )

    if post.author != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorised to delete this post",
        )

    db.delete(post)
    db.commit()

    return "Post deleted successfully"

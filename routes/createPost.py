from fastapi import APIRouter, Depends, HTTPException, status
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

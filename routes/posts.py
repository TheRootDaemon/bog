"""
posts.py

This module provides routes related to post management:
- Creating, updating, and deleting posts
- Liking and unliking posts

All operations are authenticated and scoped to the current user.
"""

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


@router.post(
    "",
    summary="Creates a post",
    description="Creates a post for the current user",
    response_model=postResponse,
)
def createPost(
    postData: postMetadata,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Creates a new post authored by the current user.

    Args:
        postData (postMetadata): Post content and title.
        db (Session): SQLAlchemy session.
        current_user (User): Authenticated user.

    Returns:
        postResponse: The created post object.
    """
    post = Post(author=current_user.id, title=postData.title, content=postData.content)

    db.add(post)
    db.commit()
    db.refresh(post)

    return post


@router.put(
    "/{post_id}",
    summary="Updates a post",
    description="Updates a post for the current user",
    response_model=postResponse,
)
def updatePost(
    post_id: int,
    postData: postMetadata,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Updates a post owned by the current user.

    Args:
        post_id (int): ID of the post to update.
        postData (postMetadata): New title and content.
        current_user (User): Authenticated user.
        db (Session): SQLAlchemy session.

    Returns:
        postResponse: Updated post object.

    Raises:
        HTTPException:
            - 400 if post not found.
            - 403 if the user is not the author.
    """
    post = db.query(Post).filter(Post.id == post_id).first()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Post not found"
        )

    if post.author != current_user.id:  # type:ignore
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorised to delete this post",
        )

    post.title = postData.title  # type:ignore
    post.content = postData.conten  # type:ignore

    db.commit()
    db.refresh(post)

    return post


@router.delete(
    "/{post_id}",
    summary="Deletes a post",
    description="Deletes a post for the current user",
)
def deletePost(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Deletes a post owned by the current user.

    Args:
        post_id (int): ID of the post to delete.
        db (Session): SQLAlchemy session.
        current_user (User): Authenticated user.

    Returns:
        str: Deletion confirmation message.

    Raises:
        HTTPException:
            - 404 if post not found.
            - 403 if the user is not the author.
    """
    post = db.query(Post).filter(Post.id == post_id).first()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not Found"
        )

    if post.author != current_user.id:  # type:ignore
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorised to delete this post",
        )

    db.delete(post)
    db.commit()

    return "Post deleted successfully"


@router.post(
    "/{post_id}/like",
    summary="Likes a post",
)
def likePost(
    post_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Allows the current user to like a post.

    Args:
        post_id (int): ID of the post to like.
        current_user (User): Authenticated user.
        db (Session): SQLAlchemy session.

    Returns:
        dict: Success message.

    Raises:
        HTTPException:
            - 400 if post/user not found or already liked.
    """
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
    "/{post_id}/like",
    summary="Unlikes a post",
)
def unlikePost(
    post_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Allows the current user to unlike a previously liked post.

    Args:
        post_id (int): ID of the post to unlike.
        current_user (User): Authenticated user.
        db (Session): SQLAlchemy session.

    Returns:
        dict: Success message.

    Raises:
        HTTPException:
            - 400 if post/user not found or not liked yet.
    """
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

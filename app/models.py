"""
models.py

This module defines the SQLAlchemy ORM models for a simple social media-like platform.
It includes users, posts, and many-to-many relationship tables for followers and likes.

Tables:
- Users
- Posts
- follow (association table for followers)
- likes (association table for post likes)
"""

from sqlalchemy import (Column, ForeignKey, Integer, String, Table,
                        Text)
from sqlalchemy.orm import relationship

from .database import Base

follow = Table(
    "follow",
    Base.metadata,
    Column("follower", Integer, ForeignKey("Users.id"), primary_key=True),
    Column("followee", Integer, ForeignKey("Users.id"), primary_key=True),
)

likes = Table(
    "likes",
    Base.metadata,
    Column("likedBy", Integer, ForeignKey("Users.id"), primary_key=True),
    Column("likedPost", Integer, ForeignKey("Posts.id"), primary_key=True),
)


class User(Base):
    """
    ORM model representing a user in the system.

    Attributes:
        id (int): Primary key.
        username (str): Unique username.
        email (str): Email address of the user.
        gender (str): Gender of the user.
        password (str): Hashed password.
        followers (List[User]): Users who follow this user.
        following (List[User]): Users this user is following.
        posts (List[Post]): Posts authored by the user.
        likedPosts (List[Post]): Posts liked by the user.
    """
    __tablename__ = "Users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, nullable=False)
    gender = Column(String)
    password = Column(String, nullable=False)

    followers = relationship(
        "User",
        secondary=follow,
        primaryjoin=id == follow.c.followee,
        secondaryjoin=id == follow.c.follower,
        backref="following",
    )

    posts = relationship("Post", back_populates="users")

    likedPosts = relationship("Post", secondary=likes, back_populates="liked")


class Post(Base):
    """
    ORM model representing a post in the system.

    Attributes:
        id (int): Primary key.
        author (int): ID of the user who authored the post.
        title (str): Title of the post.
        content (str): Content body of the post.
        users (User): Author of the post.
        liked (List[User]): Users who liked the post.
    """
    __tablename__ = "Posts"

    id = Column(Integer, primary_key=True, index=True)
    author = Column(Integer, ForeignKey("Users.id"))
    title = Column(Text, nullable=False)
    content = Column(Text)

    users = relationship("User", back_populates="posts")

    liked = relationship("User", secondary=likes, back_populates="likedPosts")

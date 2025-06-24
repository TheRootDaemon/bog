from sqlalchemy import (Column, DateTime, ForeignKey, Integer, String, Table,
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
    __tablename__ = "Posts"

    id = Column(Integer, primary_key=True, index=True)
    author = Column(Integer, ForeignKey("Users.id"))
    title = Column(Text, nullable=False)
    content = Column(Text)

    users = relationship("User", back_populates="posts")

    liked = relationship("User", secondary=likes, back_populates="likedPosts")

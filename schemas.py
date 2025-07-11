"""
schemas.py

This module defines Pydantic models for request and response validation
in the API. These models enforce data structure and type validation
for operations related to users, authentication, and posts.
"""

from pydantic import BaseModel, EmailStr


class userMetadata(BaseModel):
    username: str
    email: EmailStr
    gender: str
    password: str


class registrationResponse(BaseModel):
    id: int
    username: str
    email: str
    gender: str


class Token(BaseModel):
    access_token: str
    token_type: str


class postMetadata(BaseModel):
    title: str
    content: str

    class Config:
        orm_mode = True


class postResponse(BaseModel):
    id: int
    author: int
    title: str
    content: str

    class Config:
        orm_mode = True


class userSummary(BaseModel):
    id: int
    username: str
    gender: str
    followersCount: int

    class Config:
        orm_mode = True

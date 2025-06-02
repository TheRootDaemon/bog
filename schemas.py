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

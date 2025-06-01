from pydantic import BaseModel, EmailStr


class userMetadata(BaseModel):
    username: str
    email: EmailStr
    gender: str
    password: str

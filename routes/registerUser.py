from fastapi import APIRouter, Body, Depends, HTTPException, status
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter(
    prefix="/users",
    tags=["Users_Test"],
)


@router.post(
    "/registerUser",
    status_code=status.HTTP_201_CREATED,
    summary="Creates, registers a user",
    description="Creates a User in the datase with necessary hashing",
)
def createUser(
    username: str = Body(..., enbed=True),
    password: str = Body(..., embed=True),
    db: Session = Depends(get_db),
):
    existingUsers = db.query(User.username).filter(User.username == username).first()
    if existingUsers:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already exists",
        )

    new_user = User(username=username, password=pwd_context.hash(password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "User Created successfully",
        "id": new_user.id,
        "username": new_user.username,
        "stored_password": new_user.password,
    }

from code.database import get_db
from code.models import User

from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status, Body

router = APIRouter(
    prefix="/users",
    tags=["Users_Test"],
)

@router.post(
        "/createUser",
        status_code=status.HTTP_201_CREATED,
        summary="Creates a test User",
        description="Creates a User without any type of validation or hashing"
)
def createUser(
    username: str = Body(..., enbed=True),
    password: str = Body(..., embed=True),
    db: Session = Depends(get_db)
):
    existingUsers = db.query(User.username).filter(User.username == username).first()
    if existingUsers:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
                detail = "User already exists",
        )
    
    new_user = User(username=username, password=password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "User Created successfully",
        "id": new_user.id,
        "username": new_user.username,
        "stored_password": new_user.password
    }

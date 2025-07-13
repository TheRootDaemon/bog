"""
auth.py

This module handles user authentication using JWT in a FastAPI application.

Functionalities:
- User login via username and password.
- Secure password hashing and verification using bcrypt.
- JWT token generation for authenticated sessions.
- Retrieval of the current user from a JWT token.
"""

from datetime import datetime, timedelta, timezone
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import User
from ..schemas import Token

router = APIRouter(
    prefix="/auth",
    tags=["Authenitication"],
)

oauth2_bearer = OAuth2PasswordBearer("/auth/token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = "sjgfnsfngsjdfnskndfglksndflgnsdlfgnlsdkngfsdlkfngslkdnfglskdnfgklsndflknsdlknldsknh"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


@router.post(
    "/token", response_model=Token, summary="Generates a JWT Token for the User"
)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    """
    Authenticates user credentials and returns a JWT access token.

    Args:
        form_data (OAuth2PasswordRequestForm): Form containing username and password.
        db (Session): SQLAlchemy session dependency.

    Returns:
        Token: JWT token and its type if authentication is successful.

    Raises:
        HTTPException: If authentication fails.
    """
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate user",
        )
    access_token = create_access_token(user.username, user.id)
    return {"access_token": access_token, "token_type": "bearer"}


def authenticate_user(username: str, password: str, db):
    """
    Validates the username and password against the database.

    Args:
        username (str): Username provided by the client.
        password (str): Raw password to verify.
        db (Session): Database session.

    Returns:
        User: The authenticated user object.

    Raises:
        HTTPException: If the user is not found or the password is incorrect.
    """
    user = db.query(User).filter(User.username == username).first()
    if not user or not pwd_context.verify(password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user"
        )
    return user


def create_access_token(username, id):
    """
    Creates a JWT token with the specified username and user ID.

    Args:
        username (str): Username to encode in token.
        id (int): User ID to encode in token.

    Returns:
        str: JWT access token.
    """
    to_encode = {"sub": username, "id": id}
    expire = datetime.now(timezone.utc).replace(tzinfo=None) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(
    token: Annotated[str, Depends(oauth2_bearer)], db: Session = Depends(get_db)
):
    """
    Retrieves the current authenticated user from the JWT token.

    Args:
        token (str): JWT token extracted from the request header.
        db (Session): SQLAlchemy session dependency.

    Returns:
        User: Authenticated user object.

    Raises:
        HTTPException: If the token is invalid or user not found.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        id = payload.get("id")
        if username is None or id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate user",
            )
        user = db.query(User).filter(User.id == id).first()
        return user
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user"
        )

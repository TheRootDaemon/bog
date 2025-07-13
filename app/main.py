"""
main.py

This is the entry point of the FastAPI application.

Functionalities:
- Initializes FastAPI app.
- Creates all database tables.
- Defines root-level endpoints for API health check and authentication test.
- Includes all modular routers: user registration, authentication, feed, follow, and posts.

Routes:
- GET /               — Returns API health status.
- GET /user           — Returns current authenticated user.
- /users/*            — Handles user registration and following/unfollowing.
- /auth/*             — Handles JWT login and token-based authentication.
- /feed/*             — Fetches user and post feeds.
- /posts/*            — Manages post creation, update, deletion, and likes.
"""

from fastapi import Depends, FastAPI

from .database import Base, engine
from .routes import auth, feed, follow, posts, registerUser
from .routes.auth import get_current_user

app = FastAPI()
Base.metadata.create_all(bind=engine)


@app.get("/", summary="Gets API's status", tags=["Root"])
def default():
    """
    Root endpoint to verify if the API is running.

    Returns:
        dict: A status message confirming the API is active.
    """
    return {"message": "The bog is active"}


@app.get("/user", summary="Returns the authenticated user", tags=["Root"])
def user(user: dict = Depends(get_current_user)):
    """
    Returns the currently authenticated user from the JWT token.

    Args:
        user (dict): Injected user object via token-based authentication.

    Returns:
        dict: Success message with user data.
    """
    return {"message": "You are authorised", "user": user}


# Modularized functional Routers that make up the API
app.include_router(registerUser.router)
app.include_router(auth.router)
app.include_router(feed.router)
app.include_router(follow.router)
app.include_router(posts.router)

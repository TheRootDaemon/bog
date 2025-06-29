from fastapi import Depends, FastAPI

from .database import Base, engine
from .routes import auth, feed, follow, likePost, posts, registerUser
from .routes.auth import get_current_user

app = FastAPI()
Base.metadata.create_all(bind=engine)


@app.get("/", summary="Gets API's status", tags=["Root"])
def default():
    return {"message": "The API is UP and running ..."}


@app.get("/user", summary="Returns the authenticated user", tags=["Root"])
def user(user: dict = Depends(get_current_user)):
    return {"message": "You are authorised", "user": user}


app.include_router(registerUser.router)
app.include_router(auth.router)
app.include_router(feed.router)
app.include_router(follow.router)
app.include_router(posts.router)
app.include_router(likePost.router)

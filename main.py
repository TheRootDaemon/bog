from fastapi import Depends, FastAPI

from .database import Base, engine
from .routes import auth, feed, follow, likePost, posts, registerUser
from .routes.auth import get_current_user

app = FastAPI()
Base.metadata.create_all(bind=engine)

app.include_router(registerUser.router)
app.include_router(auth.router)
app.include_router(follow.router)
app.include_router(posts.router)
app.include_router(likePost.router)
app.include_router(feed.router)


@app.get("/", summary="Returns the authenticated user")
def user(user: dict = Depends(get_current_user)):
    return {"message": "You are authorised", "user": user}

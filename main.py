from fastapi import Depends, FastAPI

from .database import Base, engine
from .routes import auth, registerUser
from .routes.auth import get_current_user

app = FastAPI()
Base.metadata.create_all(bind=engine)

app.include_router(registerUser.router)
app.include_router(auth.router)


@app.get("/")
def user(user: dict = Depends(get_current_user)):
    return {"message": "You are authorised", "user": user}

from fastapi import FastAPI

from .database import Base, engine
from .routes import auth, registerUser

app = FastAPI()
Base.metadata.create_all(bind=engine)

app.include_router(registerUser.router)
app.include_router(auth.router)


@app.get("/")
def root():
    return {"message": "The API is up my brother...."}

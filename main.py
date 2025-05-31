from fastapi import FastAPI

from .database import Base, engine
from .routes import registerUser

app = FastAPI()
Base.metadata.create_all(bind=engine)

app.include_router(registerUser.router)


@app.get("/")
def root():
    return {"message": "The API is up my brother...."}

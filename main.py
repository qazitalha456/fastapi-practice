from fastapi import FastAPI
from routes import auth
from routes import posts, user
from schema import  *
from models import *
from  database import engine

Base.metadata.create_all(bind=engine)

app = FastAPI()

# Routes
app.include_router(
    posts.router,
    prefix="/api",
    tags=["Posts"]
)
app.include_router(
    user.router,
    prefix="/api",
    tags=["Users"]
)   
app.include_router(
    auth.router,
    prefix="/api",
    tags=["Authentication"]
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
from typing import Annotated
from fastapi import FastAPI, Response, status, HTTPException,Depends
from fastapi.security import OAuth2PasswordRequestForm
import psycopg2
from psycopg2.extras import RealDictCursor
import time
import hashing, outh2
from routes import auth
from routes import posts, user
from schema import  *
from models import *
from  database import engine,get_db



Base.metadata.create_all(bind=engine)

app = FastAPI()

while True:
    try:
        conn = psycopg2.connect(host='localhost', database='Fastapi project', user='postgres',
                                password='5432', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was succesfull!")
        break
    except Exception as error:
        print("Connecting to database failed")
        print("Error: ", error)
        time.sleep(2)
        



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
    tags=["Users"]
)
from sqlalchemy.orm import Session

@app.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    
    print("Received login request with form data:", form_data)
    print("Email:", form_data.username)
    print("Password:", form_data.password)

    db: Session = next(get_db())
    user = db.query(User_model).filter(User_model.email == form_data.username).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")
    
    if not hashing.verify_password(form_data.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")
    
    access_token = outh2.create_access_token(data={"user_id": user.id})
    
    return {"access_token": access_token, "token_type": "bearer"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
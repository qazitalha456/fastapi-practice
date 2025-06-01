from fastapi import FastAPI, Response, status, HTTPException,Depends
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from schema import  *
from models import *
from  database import engine,get_db
from database import sessionlocal,get_db
from sqlalchemy.orm import Session
from pydantic import BaseModel
import bcrypt
from fastapi import APIRouter
router = APIRouter()
@router.post("/users", status_code=status.HTTP_201_CREATED,tags=["Users"])
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # Hash the password
    hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())
    user_data = user.dict()
    user_data['password'] = hashed_password.decode('utf-8')
    new_user = User_model(**user_data)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"data": new_user}
# ...existing code...
@router.get("/users/{id}")
def get_user(id: int, db: Session = Depends(get_db),tags=["Users"]):
    user = db.query(User_model).filter(User_model.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} not found")
    return {"data": user}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

import hashing, outh2
from schema import Token, UserLogin
from models import User_model
from database import get_db


router = APIRouter(tags=['Authentication'])

@router.post("/login", response_model=Token)
def login(user_credentials: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User_model).filter(User_model.email == user_credentials.email).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")
    
    if not hashing.verify_password(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")
    
    access_token = outh2.create_access_token(data={"user_id": user.id})
    
    return {"access_token": access_token, "token_type": "bearer"}

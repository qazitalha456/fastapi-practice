from typing import Annotated
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

import hashing, outh2
from schema import Token, UserLogin
from models import User_model
from database import get_db


router = APIRouter(tags=['Authentication'])

from sqlalchemy.orm import Session

@router.post("/login", response_model=Token, status_code=status.HTTP_200_OK)
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

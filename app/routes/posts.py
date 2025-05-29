from fastapi import FastAPI, Response, status, HTTPException,Depends
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
import outh2
from schema import  *
from models import *
from  database import engine,get_db
from database import sessionlocal,get_db
from sqlalchemy.orm import Session
from pydantic import BaseModel
from fastapi import FastAPI, Depends



from fastapi import APIRouter
router = APIRouter()

@router.get("/posts",tags=["Posts"])
async def read_posts(db: Session = Depends(get_db),current_user: int = Depends(outh2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    posts = db.query(Post_model).all()

    return {"data": posts}

@router.post("/posts", status_code=status.HTTP_201_CREATED,tags=["Posts"])
def create_posts(post: Post):
    post_dict = post.dict()
    post_dict['id'] = randrange(0, 1000000)
    # Add to the database
    new_post = Post_model(**post_dict)
    db = next(get_db())
    db.add(new_post)
    db.commit()
    return {"data": post_dict}


@router.get("/posts/{id}",tags=["Posts"])
def get_post(id: int,db: Session = Depends(get_db)):
    new_post = db.query(Post_model).filter(Post_model.id == id).first()
    if not new_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
    return {"data_detail": new_post}

@router.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT,tags=["Posts"])
def delete_post(id: int,db: Session = Depends(get_db)):
    

    db.query(Post_model).filter(Post_model.id == id).delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/posts/{id}",tags=["Posts"])
def update_post(id: int, post: Post,db: Session = Depends(get_db)):
    index = db.query(Post_model).filter(Post_model.id == id).first()
    if not index:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
    updated_post = post.dict()
    updated_post["id"] = id
    
    db.query(Post_model).filter(Post_model.id == id).update(updated_post, synchronize_session=False)
    db.commit()

    return {"message": f"Post with id {id} updated successfully", "data": updated_post}

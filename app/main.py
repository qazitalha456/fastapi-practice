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
@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/posts")
async def read_posts(db: Session = Depends(get_db)):
    posts = db.query(Post_model).all()

    return {"data": posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    post_dict = post.dict()
    post_dict['id'] = randrange(0, 1000000)
    # Add to the database
    new_post = Post_model(**post_dict)
    db = next(get_db())
    db.add(new_post)
    db.commit()
    return {"data": post_dict}


@app.get("/posts/{id}")
def get_post(id: int,db: Session = Depends(get_db)):
    new_post = db.query(Post_model).filter(Post_model.id == id).first()
    if not new_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
    return {"data_detail": new_post}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int,db: Session = Depends(get_db)):
    

    db.query(Post_model).filter(Post_model.id == id).delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: int, post: Post,db: Session = Depends(get_db)):
    index = db.query(Post_model).filter(Post_model.id == id).first()
    if not index:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
    updated_post = post.dict()
    updated_post["id"] = id
    
    db.query(Post_model).filter(Post_model.id == id).update(updated_post, synchronize_session=False)
    db.commit()

    return {"message": f"Post with id {id} updated successfully", "data": updated_post}
# make a user route 
import bcrypt
# ...existing code...

@app.post("/users", status_code=status.HTTP_201_CREATED)
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
@app.get("/users/{id}")
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(User_model).filter(User_model.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} not found")
    return {"data": user}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
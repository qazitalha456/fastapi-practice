from fastapi import FastAPI, Response, status, HTTPException,Depends
import psycopg2
from psycopg2.extras import RealDictCursor
import time
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




if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
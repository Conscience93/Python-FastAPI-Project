"""MAIN"""

#Start server
from fastapi import Body, FastAPI, status, HTTPException
app = FastAPI()

from requests import Response
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from typing import Optional, List

# Database
from . import models
from .database import engine, get_db
models.Base.metadata.create_all(bind=engine)   #code that create a table (he thnks)

#Schemas
from . import schemas


#test posts
from sqlalchemy.orm import Session
from fastapi import Depends


while True:
    try:
        connection = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='UNMC1234', cursor_factory=RealDictCursor)
        cursor = connection.cursor()
        print("Database connection was successful.")
        break
    except Exception as error:
        print("Error: ", error)
        time.sleep(3)



@app.get("/")    # decorator
async def root():
    return {"message": "Welcome to my api"}    #FastAPI will auto convert this to json


# @app.get("/posts", response_model=schemas.Post)  response_model=schemas.Post will return error because it can't return "plain" list
@app.get("/posts", response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db)):
    """Get all posts"""
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return posts




@app.post("/createposts", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db)):
    """Create Post"""
    new_post = models.Post(**post.dict())   # Note: new_post is a SQL alchemy model, not pydantic dict.
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post




@app.get("/posts/{id}", response_model=schemas.Post)     #Note: @app.get("/posts/{id}")  {id} will return string id
def get_post(id: int, db: Session = Depends(get_db)):
    """Retrieve one individual post"""
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return post}

@app.put("/posts/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db)):
    """Update post"""
    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} does not exist.")

    post_query.update(updated_post.dict(), synchronize_session=False)

    db.commit()

    return post_query.first()


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    """Delete a post"""
    post = db.query(models.Post).filter(models.Post.id == id)

    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} does not exist.")

    post.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)



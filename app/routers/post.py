"""Post"""

from .. import models, schemas
from fastapi import Body, FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List

# Router Object
router = APIRouter(
    prefix="/posts" ,
    tags=["Posts"]        # for easy to read local fastapi documentation
)

# Database
from ..database import engine, get_db


# @app.get("/posts", response_model=schemas.Post)  response_model=schemas.Post will return error because it contains lists of posts.
# response_model is a thing that send info back to the user client
@router.get("/", response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db)):
    """Get all posts"""
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return posts




@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db)):
    """Create Post"""
    new_post = models.Post(**post.dict())   # Note: new_post is a SQL alchemy model, not pydantic dict.
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post




@router.get("/{id}", response_model=schemas.Post)     #Note: @app.get("/posts/{id}")  {id} will return string id
def get_post(id: int, db: Session = Depends(get_db)):
    """Retrieve one individual post"""
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return post

@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db)):
    """Update post"""
    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} does not exist.")

    post_query.update(updated_post.dict(), synchronize_session=False)

    db.commit()

    return post_query.first()


@router.delete("{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    """Delete a post"""
    post = db.query(models.Post).filter(models.Post.id == id)

    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} does not exist.")

    post.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
"""Post"""

from click import get_current_context
from .. import models, schemas, oauth2
from fastapi import Body, FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional

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
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user),
limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    # http://127.0.0.1:9000/posts?limit=3     if limit is specified, u should get only 3 posts. By default is 10

    """Get all posts"""
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return posts




@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    """Create Post"""
    new_post = models.Post(owner_id=current_user.id, **post.dict())   # Note: new_post is a SQL alchemy model, not pydantic dict.
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post




@router.get("/{id}", response_model=schemas.Post)     #Note: @app.get("/posts/{id}")  {id} will return string id
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    """Retrieve one individual post"""
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    # if post.owner_id != current_user.id:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorised to perform requested action.")

    return post

@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    """Update post"""
    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} does not exist.")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorised to perform requested action.")

    post_query.update(updated_post.dict(), synchronize_session=False)

    db.commit()

    return post


@router.delete("{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    """Delete a post"""
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} does not exist.")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorised to perform requested action.")

    post.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
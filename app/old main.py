from typing import Optional
from fastapi import Body, FastAPI, status, HTTPException
from pydantic import BaseModel
from requests import Response

import psycopg2
from psycopg2.extras import RealDictCursor

import time

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True

while True:
    try:
        connection = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='UNMC1234', cursor_factory=RealDictCursor)
        cursor = connection.cursor()
        print("Database connection was successful.")
        break
    except Exception as error:
        print("Error: ", error)
        time.sleep(3)



my_posts = [
    {"title":"One", "content":"hi", "id":1},
    {"title":"Two", "content":"hi2", "id":2}
]


@app.get("/")    # decorator
async def root():
    return {"message": "Welcome to my api"}    #FastAPI will auto convert this to json


@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    return {"data": posts}


@app.post("/createposts")
def create_posts(new_post: Post):    #FastAPI will auto validate the payload contents such as checking title and content names
    # cursor.execute(f"INSERT INTO posts (title, content, published) VALUES({posts.title}, {posts.content}, {posts.published})") <-- vulnerable to SQL attack. Can be edited through postman
    cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, (new_post.title, new_post.content, new_post.published))
    result = cursor.fetchone()
    connection.commit()     # Push changes into database

    return {"data": result}


@app.get("/posts/{id}")     #Note: @app.get("/posts/{id}")  {id} will return string id
def get_post(id: int):
    """Retrieve one individual post"""
    cursor.execute("""SELECT * FROM posts WHERE id = %s """, (str(id)))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} is not found.")

    return {"post_detail": f"Here is post {id}"}

@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    """Update post"""
    cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", (post.title, post.content, post.published, str(id)))
    updated_post = cursor.fetchall()
    connection.commit()

    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} does not exist.")
        
    return {"data": updated_post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    """Delete post"""
    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id)))
    deleted_post = cursor.fetchall()
    connection.commit()
    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} does not exist.")

    return {"data": delete_post}



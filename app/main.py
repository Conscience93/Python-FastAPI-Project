"""MAIN"""

#Start server
from fastapi import Body, FastAPI, status, HTTPException
app = FastAPI()

from requests import Response
import psycopg2
from psycopg2.extras import RealDictCursor
import time

# Router - https://www.fastapitutorial.com/blog/fastapi-route/
from .routers import post, user, auth
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

# Database
from . import models
from .database import engine, get_db
models.Base.metadata.create_all(bind=engine)   #code that create a table (he thnks)

# Password
import utils

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




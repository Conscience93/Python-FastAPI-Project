"""MAIN"""

#Start server
from fastapi import FastAPI
app = FastAPI()

# Router - https://www.fastapitutorial.com/blog/fastapi-route/
from .routers import post, user, auth
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

# Database
from . import models
from .database import engine
models.Base.metadata.create_all(bind=engine)   #code that create a table (he thinks)


@app.get("/")    # decorator
async def root():
    return {"message": "Welcome to my api"}    #FastAPI will auto convert this to json




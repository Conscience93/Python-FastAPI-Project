"""MAIN"""

#Start server
from fastapi import FastAPI
app = FastAPI()

# CORS middleware - https://fastapi.tiangolo.com/id/tutorial/cors/
from fastapi.middleware.cors import CORSMiddleware
origins = ["*"]

app.add_middleware(
    CORSMiddleware, 
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Router - https://www.fastapitutorial.com/blog/fastapi-route/
from .routers import post, user, auth, vote
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

# Database
from . import models
from .database import engine
# models.Base.metadata.create_all(bind=engine)   #code that create a table (he thinks). Since there's already alembic, this line is not needed

# pydantic
from .config import Settings

@app.get("/")    # decorator
async def root():
    return {"message": "Welcome to my api"}    #FastAPI will auto convert this to json




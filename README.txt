# Python-FastAPI-Project
Using FastAPI as a tool for Python API Development. Courtesy of FreeCodeCamp Youtube.

# V1.0 - 2/6/2022
- Created Python FAST API from scratch up to testing database connection with Postgres.

# V1.1 - 3/6/2022
- Add Post model User, user_create and get_user function, hashing function.
- Clean up main.py, spliting post and user functions into two different files in routers.
- Add JWT token authentication system.

Start-up
venv/Scripts/Activate.ps1
uvicorn app.main:app --reload
# Python-FastAPI-Project
Using FastAPI as a tool for Python API Development. Courtesy of FreeCodeCamp Youtube.

## V1.0 - 2/6/2022
- Created Python FAST API from scratch up to testing database connection with Postgres.

## V1.1 - 15/6/2022
- Add Post model User, user_create and get_user function, hashing function.
- Clean up main.py, spliting post and user functions into two different files in routers.
- Add JWT token authentication system.

## V1.2 - 17/6/2022
- Add Foreign Key in post model that is connected to user model.
- Implement simple authorisation (Improving oauth2) so posts can only be changed by their owner.
- Clean up main.py part 2

## V1.3 - 19/6/2022
- Add .env and .gitignore files (should have put that. Oops)
- Replacing sensitive information with env reference.
- Add pydantic for env value validation.

Start-up
venv/Scripts/Activate.ps1
uvicorn app.main:app --reload
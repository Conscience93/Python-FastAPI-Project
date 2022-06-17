"""Auth using JWT Tokens"""
# https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/

from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from .. import database, schemas, models, utils, oauth2

router = APIRouter(tags=['authentication'])


@router.post('/login', response_model=schemas.Token)
# def login(user_credentials: schemas.UserLogin, db: Session = Depends(database.get_db)):
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    
    # OAuth2PasswordRequestForm contains username and password only, not email, so user_credentials.email has to be changed into username.
    # In Postman, instead of sending data raw, we now have to send in form-data format.
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")

    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")

    # create a jwt token
    access_token = oauth2.create_access_token(data = {"user_id": user.id})

    # return the token
    return {"access_token": access_token, "token_type": "bearer"}
    
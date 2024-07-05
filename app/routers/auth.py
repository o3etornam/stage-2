from typing import List
from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models
from .. import schema
from .. import utlis
from .. import oauth2


router = APIRouter(
    prefix='/auth',
    tags=['Authentication']
)

@router.post('/login', response_model=schema.Token)
async def login(user_credentials: OAuth2PasswordRequestForm = Depends()
                ,db:Session = Depends(get_db)):
    # OAuth2PasswordRequestFor stores what the user enters in a dictionary 
    # w key words username and password
    user = db.query(models.User).filter(models.User.email == user_credentials.username)
    
    if user:
        if await utlis.verify(user_credentials.password, user.password):
            access_token = await oauth2.create_access_token(data = {'user_id':user.userId})
            return schema.Token(accessToken=access_token)
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='invalid credentials')
    
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                         detail=f'user with email {user_credentials.username} not found')
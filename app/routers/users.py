from typing import List
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models
from .. import schema
from .. import utlis



router = APIRouter(
    prefix='/api',
    tags= ['Users']
)


@router.get('/users', response_model= List[schema.User])  
async def get_users(db:Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users

@router.get('users/{id}', response_model= schema.User)
async def get_user(id: int, db:Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.userId == id).first()
    if user:
        return user
    raise HTTPException(status_code=404, detail=f'User with id {id} doesn\'t exsit')
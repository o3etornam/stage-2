from typing import List
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models
from .. import schema
from .. import utlis



router = APIRouter(
    prefix='/auth/register',
    tags= ['Register']
)


@router.post('', status_code=201, response_model=schema.UserPublic)
def create_user(user: schema.UserCreate, db:Session = Depends(get_db)):
    user.password = utlis.hash(user.password)
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
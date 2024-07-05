
import jwt
from jwt.exceptions import InvalidTokenError
from datetime import datetime, timedelta, timezone
from . import database, models
from sqlalchemy.orm import Session
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from . config import settings
from typing import Annotated


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

def create_access_token(data: dict):
    to_encode = data.copy() 

    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({'exp':expire})

    encoded_jwt = jwt.encode(to_encode, key = SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def verify_acces_token(token: str, credential_exception):
    try:
        payload = jwt.decode(jwt=token, key=SECRET_KEY, algorithms=[ALGORITHM])

        user_id: str = str(payload.get("user_id"))

        if user_id:
            return user_id
        raise credential_exception
    except InvalidTokenError:
        raise credential_exception
    
async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)],
                     db: Session = Depends(database.get_db)):
    
    credentials_exception = HTTPException(status_code= status.HTTP_401_UNAUTHORIZED, detail='could not validate credentials',
                                          headers={'WWW-Authenticate':'Bearer'})
    
    user_id = await verify_acces_token(token, credentials_exception)
    user = db.query(models.User).filter(models.User.userId == int(user_id))
    return user
    
from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models
from .. import schema
from .. import utlis
from .. import oauth2


router = APIRouter(tags=["Authentication"])


@router.post("/auth/login", response_model=schema.UserPublic)
def login(
    user_credentials: schema.UserLogin,
    db: Session = Depends(get_db),
):
    user = (
        db.query(models.Users)
        .filter(models.Users.email == user_credentials.email)
        .first()
    )

    if user:
        if utlis.verify(user_credentials.password, user.password):
            access_token = oauth2.create_access_token(data={"user_id": user.userId})
            return schema.UserPublic(
                message="Login Successful",
                data=schema.Data(
                    accessToken=access_token,
                    user=schema.User(
                        userId=str(user.userId),
                        firstName=user.firstName,
                        lastName=user.lastName,
                        email=user.email,
                        phone=user.phone,
                    ),
                ),
            )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "status": "Bad request",
                "message": "Authentication failed",
                "statusCode": 401,
            },
        )

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail={
            "status": "Bad request",
            "message": "Authentication failed",
            "statusCode": 401,
        },
    )


@router.post("/login", response_model=schema.TokenData)
def token_login(
    user_credentials: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = (
        db.query(models.Users)
        .filter(models.Users.email == user_credentials.username)
        .first()
    )

    if user:
        if utlis.verify(user_credentials.password, user.password):
            access_token = oauth2.create_access_token(data={"user_id": user.userId})
            return schema.TokenData(access_token=access_token)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "status": "Bad request",
                "message": "Authentication failed",
                "statusCode": 401,
            },
        )

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail={
            "status": "Bad request",
            "message": "Authentication failed",
            "statusCode": 401,
        },
    )

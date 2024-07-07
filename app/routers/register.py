from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models
from .. import schema
from .. import utlis
from .. import oauth2


router = APIRouter(prefix="/auth/register", tags=["Register"])


@router.post("", status_code=201, response_model=schema.UserPublic)
def create_user(user: schema.UserCreate, db: Session = Depends(get_db)):
    user.password = utlis.hash(user.password)
    try:
        new_user = models.Users(**user.model_dump())
        new_organisation = models.Organisations(
            name=f"{new_user.firstName}'s Organisation"
        )

        db.add(new_user)
        db.add(new_organisation)
        db.commit()

        db.refresh(new_user)
        db.refresh(new_organisation)

        new_member = models.Members(
            orgId=new_organisation.orgId, userId=new_user.userId
        )
        db.add(new_member)
        db.commit()
        db.refresh(new_member)

        access_token = oauth2.create_access_token(data={"user_id": new_user.userId})
        return schema.UserPublic(
            message="Registration Successful",
            data=schema.Data(
                accessToken=access_token,
                user=schema.User(
                    userId=str(new_user.userId),
                    firstName=new_user.firstName,
                    lastName=new_user.lastName,
                    email=new_user.email,
                    phone=new_user.phone,
                ),
            ),
        )
    except Exception:
        raise HTTPException(
            status_code=400,
            detail={
                "status": "Bad request",
                "message": "Registration unsuccessful",
                "statusCode": 400,
            },
        )

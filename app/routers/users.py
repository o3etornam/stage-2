from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models
from .. import schema
from .. import oauth2


router = APIRouter(prefix="/api", tags=["Users"])


@router.get("/users/{id}")
async def get_user(
    id: int,
    db: Session = Depends(get_db),
    current_user: schema.User = Depends(oauth2.get_current_user),
):
    organisations = (
        db.query(models.Members)
        .filter(models.Members.userId == current_user.userId)
        .all()
    )
    user = db.query(models.Users).filter(models.Users.userId == id).first()
    if user:
        for org in organisations:
            if (
                db.query(models.Members)
                .filter(
                    models.Members.orgId == org.orgId,
                    models.Members.userId == user.userId,
                )
                .first()
            ):
                return {
                    "status": "success",
                    "message": "<message>",
                    "data": schema.User(
                        userId=str(user.userId),
                        firstName=user.firstName,
                        lastName=user.lastName,
                        email=user.email,
                        phone=user.phone,
                    ),
                }
        raise HTTPException(
            status_code=403, detail=f"Can't access credentials of user with {id}"
        )

    raise HTTPException(status_code=404, detail=f"User with id {id} doesn't exsit")

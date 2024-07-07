from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models
from .. import schema
from .. import oauth2


router = APIRouter(prefix="/api/organisations", tags=["Organisations"])


@router.get("")
async def get_organizations(
    db: Session = Depends(get_db),
    current_user: schema.User = Depends(oauth2.get_current_user),
):
    organisations = (
        db.query(models.Members)
        .filter(models.Members.userId == current_user.userId)
        .all()
    )
    if organisations:
        organisations = [org.organisation for org in organisations]
        return {
            "status": "success",
            "message": "<message>",
            "organizations": organisations,
        }

    raise HTTPException(status_code=404, detail="User with id doesn't exsit")


@router.get("/{id}")
async def get_organization(
    id: int,
    db: Session = Depends(get_db),
    current_user: schema.User = Depends(oauth2.get_current_user),
):
    organisation = (
        db.query(models.Members)
        .filter(
            models.Members.userId == current_user.userId, models.Members.orgId == id
        )
        .first()
    )
    if organisation:
        return {
            "status": "success",
            "message": "<message>",
            "data": organisation.organisation,
        }

    raise HTTPException(
        status_code=404,
        detail={
            "status": "Bad request",
            "message": f"Organization with {id} not found",
            "statusCode": 404,
        },
    )


@router.post("", status_code=201)
async def create_organization(
    new_organisation: schema.OrganisationCreate,
    db: Session = Depends(get_db),
    current_user: schema.User = Depends(oauth2.get_current_user),
):
    try:
        new_organisation = models.Organisations(**new_organisation.model_dump())
        db.add(new_organisation)
        db.commit()
        db.refresh(new_organisation)
        new_member = models.Members(
            orgId=new_organisation.orgId, userId=current_user.userId
        )
        db.add(new_member)
        db.commit()
        setattr(new_organisation, "orgId", str(new_organisation.orgId))
        return schema.OrganisationPublic(data=new_organisation)
    except Exception:
        raise HTTPException(
            status_code=400,
            detail={
                "status": "Bad Request",
                "message": "Client error",
                "statusCode": 400,
            },
        )


@router.post("/{orgId}/users")
async def add_user(
    orgId: int,
    user: schema.AddUser,
    db: Session = Depends(get_db),
    current_user: schema.User = Depends(oauth2.get_current_user),
):
    organisation = (
        db.query(models.Members)
        .filter(
            models.Members.userId == current_user.userId, models.Members.orgId == orgId
        )
        .first()
    )
    if organisation:
        new_org_member = (
            db.query(models.Users).filter(models.Users.userId == user.userId).first()
        )
        if new_org_member:
            if (
                db.query(models.Members)
                .filter(
                    models.Members.userId == new_org_member.userId,
                    models.Members.orgId == orgId,
                )
                .first()
            ):
                raise HTTPException(status_code=409, detail="user is already a member")
            else:
                new_member = models.Members(orgId=orgId, userId=new_org_member.userId)
                db.add(new_member)
                db.commit()
                return {
                    "status": "success",
                    "message": "User added to organisation successfully",
                }
        raise HTTPException(
            status_code=404, detail=f"User with id {user.userId} not found"
        )
    raise HTTPException(status_code=403, detail="Forbidden Action")

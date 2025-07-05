from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from app import schemas, crud, models, deps
from typing import List
from pydantic import BaseModel

router = APIRouter()

@router.post("/", response_model=schemas.Resource)
def create_resource(resource_in: schemas.ResourceCreate, db: Session = Depends(deps.get_db), current_user: models.User = Depends(deps.get_current_user)):
    return crud.create_resource(db, resource_in, owner_id=current_user.id)

@router.get("/{resource_id}", response_model=schemas.Resource)
def get_resource(resource_id: int, db: Session = Depends(deps.get_db), current_user: models.User = Depends(deps.get_current_user)):
    resource = db.query(models.Resource).filter(models.Resource.id == resource_id).first()
    if not resource:
        raise HTTPException(status_code=404, detail="Resource not found")
    return resource

@router.get("/org/{org_id}", response_model=List[schemas.Resource])
def list_resources_in_org(org_id: int, db: Session = Depends(deps.get_db), current_user: models.User = Depends(deps.get_current_user)):
    return db.query(models.Resource).filter(models.Resource.org_id == org_id).all()

class TokenRequest(BaseModel):
    token: str

@router.delete("/delete-by-token", response_model=dict)
def delete_resource_by_token(token_req: TokenRequest, db: Session = Depends(deps.get_db)):
    token = token_req.token
    # Find the guest link by token
    guest_link = db.query(models.GuestLink).filter(models.GuestLink.token == token).first()
    if not guest_link:
        return {"success": False, "detail": "Invalid token"}
    resource = db.query(models.Resource).filter(models.Resource.id == guest_link.resource_id).first()
    if not resource:
        return {"success": False, "detail": "Resource not found"}
    db.delete(resource)
    db.commit()
    return {"success": True, "detail": "Resource deleted successfully"}

class ResourceDetail(BaseModel):
    id: int
    org_name: str
    dept_name: str
    resource_name: str
    content: str
    role: str
    expire_date: str

@router.get("/all/org/{org_id}", response_model=List[ResourceDetail])
def all_resources_in_org(org_id: int, db: Session = Depends(deps.get_db), current_user: models.User = Depends(deps.get_current_user)):
    resources = db.query(models.Resource).filter(models.Resource.org_id == org_id).all()
    result = []
    for res in resources:
        org_name = res.org.name if res.org else "-"
        dept_name = res.dept.name if res.dept else "-"
        # Find role assignment for this user and resource
        role_assignment = db.query(models.RoleAssignment).filter_by(user_id=current_user.id, resource_id=res.id).first()
        role = role_assignment.role.value if role_assignment else "-"
        # Find guest link for this resource (for expire date)
        guest_link = db.query(models.GuestLink).filter_by(resource_id=res.id).first()
        expire_date = guest_link.expires_at.strftime('%Y-%m-%d %H:%M') if guest_link and guest_link.expires_at else "-"
        result.append(ResourceDetail(
            id=res.id,
            org_name=org_name,
            dept_name=dept_name,
            resource_name=res.name,
            content=res.content,
            role=role,
            expire_date=expire_date
        ))
    return result
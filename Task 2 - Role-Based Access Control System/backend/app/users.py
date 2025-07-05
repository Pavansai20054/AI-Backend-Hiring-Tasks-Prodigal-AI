from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas, crud, models, deps
from typing import List

router = APIRouter()

@router.get("/{user_id}", response_model=schemas.User)
def get_user(user_id: int, db: Session = Depends(deps.get_db), current_user: models.User = Depends(deps.get_current_user)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/org/{org_id}", response_model=List[schemas.User])
def list_users_in_org(org_id: int, db: Session = Depends(deps.get_db), current_user: models.User = Depends(deps.get_current_user)):
    return db.query(models.User).filter(models.User.org_id == org_id).all()

@router.post("/assign-role", response_model=schemas.RoleAssignment)
def assign_role(role_in: schemas.RoleAssignmentCreate, db: Session = Depends(deps.get_db), current_user: models.User = Depends(deps.get_current_user)):
    return crud.assign_role(db, role_in)
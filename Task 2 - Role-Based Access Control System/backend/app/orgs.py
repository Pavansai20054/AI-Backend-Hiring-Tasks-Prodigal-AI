from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas, crud, models, deps

router = APIRouter()

@router.post("/", response_model=schemas.Organization)
def create_org(org_in: schemas.OrganizationCreate, db: Session = Depends(deps.get_db), current_user: models.User = Depends(deps.get_current_user)):
    return crud.create_organization(db, org_in)

@router.get("/{org_id}", response_model=schemas.Organization)
def get_org(org_id: int, db: Session = Depends(deps.get_db), current_user: models.User = Depends(deps.get_current_user)):
    org = crud.get_organization(db, org_id)
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found")
    return org
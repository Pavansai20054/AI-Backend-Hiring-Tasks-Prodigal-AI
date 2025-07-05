from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas, crud, models, deps
from typing import Optional
from datetime import datetime

router = APIRouter()

@router.post("/share/{resource_id}", response_model=schemas.GuestLink)
def create_guest_link(resource_id: int, can_edit: bool = False, expires_at: Optional[datetime] = None, db: Session = Depends(deps.get_db), current_user: models.User = Depends(deps.get_current_user)):
    return crud.create_guest_link(db, resource_id, can_edit, expires_at)

@router.get("/access/{token}", response_model=schemas.Resource)
def access_resource_by_token(token: str, db: Session = Depends(deps.get_db)):
    link = crud.get_guest_link(db, token)
    if not link:
        raise HTTPException(status_code=404, detail="Invalid or expired guest link")
    resource = db.query(models.Resource).filter(models.Resource.id == link.resource_id).first()
    if not resource:
        raise HTTPException(status_code=404, detail="Resource not found")
    return resource
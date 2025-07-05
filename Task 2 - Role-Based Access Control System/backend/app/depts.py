from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas, crud, models, deps

router = APIRouter()

@router.post("/", response_model=schemas.Department)
def create_dept(dept_in: schemas.DepartmentCreate, db: Session = Depends(deps.get_db), current_user: models.User = Depends(deps.get_current_user)):
    return crud.create_department(db, dept_in)

# You can add more endpoints as needed, e.g., get by org, get by id, etc.
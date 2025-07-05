from sqlalchemy.orm import Session
from . import models, schemas
from passlib.context import CryptContext
from typing import Optional
import secrets
import datetime

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# User CRUD

def get_user_by_email(db: Session, email: str) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    db_user = models.User(
        email=user.email,
        hashed_password=get_password_hash(user.password),
        full_name=user.full_name,
        org_id=user.org_id,
        dept_id=user.dept_id,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Organization CRUD

def create_organization(db: Session, org: schemas.OrganizationCreate) -> models.Organization:
    db_org = models.Organization(name=org.name)
    db.add(db_org)
    db.commit()
    db.refresh(db_org)
    return db_org

def get_organization(db: Session, org_id: int) -> Optional[models.Organization]:
    return db.query(models.Organization).filter(models.Organization.id == org_id).first()

# Department CRUD

def create_department(db: Session, dept: schemas.DepartmentCreate) -> models.Department:
    db_dept = models.Department(
        name=dept.name,
        org_id=dept.org_id,
        parent_id=dept.parent_id,
    )
    db.add(db_dept)
    db.commit()
    db.refresh(db_dept)
    return db_dept

# Resource CRUD

def create_resource(db: Session, resource: schemas.ResourceCreate, owner_id: int) -> models.Resource:
    db_resource = models.Resource(
        name=resource.name,
        content=resource.content,
        owner_id=owner_id,
        org_id=resource.org_id,
        dept_id=resource.dept_id,
    )
    db.add(db_resource)
    db.commit()
    db.refresh(db_resource)
    return db_resource

# RoleAssignment CRUD

def assign_role(db: Session, assignment: schemas.RoleAssignmentCreate) -> models.RoleAssignment:
    db_assignment = models.RoleAssignment(
        user_id=assignment.user_id,
        resource_id=assignment.resource_id,
        role=assignment.role,
    )
    db.add(db_assignment)
    db.commit()
    db.refresh(db_assignment)
    return db_assignment

# GuestLink CRUD

def create_guest_link(db: Session, resource_id: int, can_edit: bool, expires_at: Optional[datetime.datetime] = None) -> models.GuestLink:
    token = secrets.token_urlsafe(16)
    db_link = models.GuestLink(
        resource_id=resource_id,
        token=token,
        can_edit=can_edit,
        expires_at=expires_at,
    )
    db.add(db_link)
    db.commit()
    db.refresh(db_link)
    return db_link

def get_guest_link(db: Session, token: str) -> Optional[models.GuestLink]:
    return db.query(models.GuestLink).filter(models.GuestLink.token == token).first()
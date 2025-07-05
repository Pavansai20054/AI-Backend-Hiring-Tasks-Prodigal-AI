from pydantic import BaseModel, EmailStr
from typing import Optional, List
import datetime
from .models import RoleEnum

class OrganizationBase(BaseModel):
    name: str

class OrganizationCreate(OrganizationBase):
    pass

class Organization(OrganizationBase):
    id: int
    class Config:
        from_attributes = True

class DepartmentBase(BaseModel):
    name: str
    org_id: int
    parent_id: Optional[int] = None

class DepartmentCreate(DepartmentBase):
    pass

class Department(DepartmentBase):
    id: int
    class Config:
        from_attributes = True

class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None

class UserCreate(UserBase):
    password: str
    org_id: int
    dept_id: Optional[int] = None

class User(UserBase):
    id: int
    is_active: bool
    org_id: int
    dept_id: Optional[int]
    class Config:
        from_attributes = True

class ResourceBase(BaseModel):
    name: str
    content: str
    org_id: int
    dept_id: Optional[int] = None

class ResourceCreate(ResourceBase):
    pass

class Resource(ResourceBase):
    id: int
    owner_id: int
    created_at: datetime.datetime
    updated_at: datetime.datetime
    class Config:
        from_attributes = True

class RoleAssignmentBase(BaseModel):
    user_id: int
    role: RoleEnum
    resource_id: Optional[int] = None

class RoleAssignmentCreate(RoleAssignmentBase):
    pass

class RoleAssignment(RoleAssignmentBase):
    id: int
    class Config:
        from_attributes = True

class GuestLinkBase(BaseModel):
    resource_id: int
    can_edit: bool = False
    expires_at: Optional[datetime.datetime] = None

class GuestLinkCreate(GuestLinkBase):
    pass

class GuestLink(GuestLinkBase):
    id: int
    token: str
    class Config:
        from_attributes = True

# Auth
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    user_id: Optional[int] = None

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class SignupRequest(UserCreate):
    pass
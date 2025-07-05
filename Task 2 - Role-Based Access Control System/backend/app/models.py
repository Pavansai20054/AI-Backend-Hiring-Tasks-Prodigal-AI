from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime, Enum, Text
from sqlalchemy.orm import relationship, declarative_base
import enum
import datetime

Base = declarative_base()

class RoleEnum(str, enum.Enum):
    admin = "admin"
    manager = "manager"
    contributor = "contributor"
    viewer = "viewer"

class Organization(Base):
    __tablename__ = "organizations"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    departments = relationship("Department", back_populates="organization")
    users = relationship("User", back_populates="organization")

class Department(Base):
    __tablename__ = "departments"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    org_id = Column(Integer, ForeignKey("organizations.id"))
    parent_id = Column(Integer, ForeignKey("departments.id"), nullable=True)
    organization = relationship("Organization", back_populates="departments")
    parent = relationship("Department", remote_side=[id])
    users = relationship("User", back_populates="department")

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    full_name = Column(String)
    is_active = Column(Boolean, default=True)
    org_id = Column(Integer, ForeignKey("organizations.id"))
    dept_id = Column(Integer, ForeignKey("departments.id"), nullable=True)
    organization = relationship("Organization", back_populates="users")
    department = relationship("Department", back_populates="users")
    roles = relationship("RoleAssignment", back_populates="user")

class Resource(Base):
    __tablename__ = "resources"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    content = Column(Text)
    owner_id = Column(Integer, ForeignKey("users.id"))
    org_id = Column(Integer, ForeignKey("organizations.id"))
    dept_id = Column(Integer, ForeignKey("departments.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    owner = relationship("User")
    org = relationship("Organization")
    dept = relationship("Department")
    guest_links = relationship("GuestLink", back_populates="resource")

class RoleAssignment(Base):
    __tablename__ = "role_assignments"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    resource_id = Column(Integer, ForeignKey("resources.id"), nullable=True)
    role = Column(Enum(RoleEnum))
    user = relationship("User", back_populates="roles")
    resource = relationship("Resource")

class GuestLink(Base):
    __tablename__ = "guest_links"
    id = Column(Integer, primary_key=True, index=True)
    resource_id = Column(Integer, ForeignKey("resources.id"))
    token = Column(String, unique=True, index=True)
    can_edit = Column(Boolean, default=False)
    expires_at = Column(DateTime, nullable=True)
    resource = relationship("Resource", back_populates="guest_links")
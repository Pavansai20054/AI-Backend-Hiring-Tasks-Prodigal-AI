from fastapi import Depends, HTTPException, status
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from jose import JWTError, jwt
from . import models, crud
from fastapi.security import OAuth2PasswordBearer
from typing import Generator
import os
import casbin
from pathlib import Path

# SQLite DB setup
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./rbac.db")
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# JWT settings
SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_enforcer():
    model_path = Path(__file__).parent / "rbac_model.conf"
    policy_path = Path(__file__).parent / "rbac_policy.csv"
    return casbin.Enforcer(str(model_path), str(policy_path))

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = int(payload.get("sub"))
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise credentials_exception
    return user

def check_permission(
    enforcer: casbin.Enforcer,
    user: models.User,
    resource: models.Resource,
    action: str
):
    # Check if user is admin
    if any(role.role == models.RoleEnum.admin for role in user.roles):
        return True
    
    # Check specific permissions
    for assignment in user.roles:
        if not enforcer.enforce(str(user.id), str(resource.id), action):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Permission denied for {action} on resource {resource.id}"
            )
    return True
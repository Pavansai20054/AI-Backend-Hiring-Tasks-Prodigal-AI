from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app import auth, orgs, depts, users, resources, guests

app = FastAPI(title="RBAC System", description="Role-Based Access Control System with Organizations, Departments, Roles, and Guest Links.")

# CORS (allow all for dev)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(orgs.router, prefix="/orgs", tags=["organizations"])
app.include_router(depts.router, prefix="/depts", tags=["departments"])
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(resources.router, prefix="/resources", tags=["resources"])
app.include_router(guests.router, prefix="/guests", tags=["guests"])

@app.get("/")
def root():
    return {"msg": "RBAC System API. See /docs for API documentation."}
# Backend - RBAC System

## Setup & Usage

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Initialize the database (SQLite)
```python
# In a Python shell:
from app.models import Base
from app.deps import engine
Base.metadata.create_all(bind=engine)
exit()
```

### 3. Run the FastAPI server
```bash
uvicorn app.main:app --reload
```
- API docs: http://localhost:8000/docs

---

## API Usage

### 1. Sign Up & Sign In
- Use `/auth/signup` and `/auth/token` endpoints.
- Copy your `access_token` from the sign in response.

### 2. Authorize in Swagger UI
- Click **Authorize** (lock icon).
- Enter your email as username, password, leave client_id/client_secret blank.

### 3. Create Organization, Department, Resource
- Use `/orgs/`, `/depts/`, `/resources/` endpoints.

### 4. Create Guest Link
- Use `POST /guests/share/{resource_id}` with your JWT token.
- Copy the `token` from the response.

### 5. Access as Guest
- Use `GET /guests/access/{token}` to view the resource as a guest.

---

## Troubleshooting
- **DB errors:** Make sure you initialized the database tables.
- **401 Unauthorized:** Authorize with a valid JWT token.
- **Bad Request:** Use your email as username, leave client_id/client_secret blank.

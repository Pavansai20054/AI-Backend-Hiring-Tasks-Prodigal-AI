# Frontend - RBAC System

## Setup & Usage

### 1. Install dependencies
```bash
npm install
```

### 2. Run the development server
```bash
npm run dev
```
- App: http://localhost:5173/

---

## User Flows

- **Sign Up:** Register a new user (requires org_id).
- **Sign In:** Log in and get a JWT token (stored in localStorage as `token`).
- **Dashboard:** Create organizations, departments, upload resources.
- **Guest Preview:** Paste a guest token to view a shared resource as a guest.

---

## How to Get Your JWT Token
- After signing in, open browser DevTools and run:
  ```js
  localStorage.getItem('token')
  ```
- Use this token for API requests if needed.

---

## Troubleshooting
- **404 error:** Make sure `index.html` is in `frontend/`, not `src/`. Run `npm run dev` from `frontend/`.
- **API errors:** Make sure the backend is running at http://localhost:8000
- **CORS errors:** Both frontend and backend must be running locally.

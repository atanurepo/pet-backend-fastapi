# User Management API (FastAPI + PostgreSQL + SCD Type‑2)

This project is a **FastAPI backend** implementing a **User Management system** with:

- PostgreSQL database
- SQLAlchemy ORM
- Pydantic schemas
- **SCD Type‑2 (Slowly Changing Dimension)** versioning
- Clean, scalable project structure

The backend automatically manages **history/versioning** of user records while exposing simple REST APIs.

---

## 1. Clone and Setup the Project

### 1.1 Clone the repository

```bash
git clone <YOUR_GITHUB_REPO_URL>
cd <repo-folder>
```

---

### 1.2 Create Python virtual environment using **uv**

This project uses **uv** for fast virtual environment and dependency management.

#### Install uv (if not installed)

```bash
pip install uv
```

#### Create virtual environment

```bash
uv venv .venv
```

#### Activate virtual environment

**Windows (PowerShell):**
```powershell
.venv\Scripts\Activate.ps1
```

**Linux / macOS:**
```bash
source .venv/bin/activate
```

---

### 1.3 Install dependencies

```bash
uv pip install -r requirements.txt
```

---

## 2. Project Folder Structure

```text
app/
├── main.py                 # FastAPI app entry point
├── core/
│   └── database.py         # DB engine, session, Base
├── models/
│   ├── base.py             # SQLAlchemy Base class
│   └── user.py             # User SQLAlchemy model (SCD‑2)
├── schemas/
│   ├── base.py             # Pydantic base config
│   └── user.py             # Pydantic schemas (Create / Read / Update)
├── crud/
│   ├── base.py             # Generic CRUD helpers
│   └── user.py             # User‑specific CRUD + SCD‑2 logic
├── api/
│   ├── deps.py             # DB dependency injection
│   └── v1/
│       ├── api.py          # API router registration
│       └── endpoints/
│           └── users.py    # User API endpoints
├── .env                    # Environment variables
└── requirements.txt        # Python dependencies
```

### Key Design Notes

- **models/** → Database tables (SQLAlchemy)
- **schemas/** → API input/output validation (Pydantic)
- **crud/** → All database interaction logic
- **api/** → HTTP routing and dependency injection
- **SCD‑2 logic** lives ONLY in `crud/user.py`

---

## 3. Automatic Table Creation

Tables are created automatically during application startup **(development only)**.

In `main.py`, SQLAlchemy runs:

```python
Base.metadata.create_all(bind=engine)
```

This will:
- Create tables if they do not exist
- Match the SQLAlchemy models

⚠️ **Production Note:**
- For production systems, use **Alembic migrations** instead of `create_all()`.

---

## 4. Running the Application

### 4.1 Set environment variables

Create a `.env` file:

```env
DATABASE_URL=postgresql+psycopg2://user:password@localhost:5432/your_db
```

---

### 4.2 Start FastAPI server

```bash
uvicorn app.main:app --reload
```

Application will be available at:

```text
http://127.0.0.1:8000
```

Swagger UI:

```text
http://127.0.0.1:8000/docs
```

Health check:

```text
GET /health
```

---

## 5. API Endpoints Examples

### 5.1 Create User (POST)

```http
POST /api/v1/users
Content-Type: application/json
```

**Request Body:**
```json
{
  "full_name": "John Doe",
  "email": "john@example.com",
  "phone": "9876543210",
  "auth_provider": "local",
  "oauth_id": "john_doe",
  "password_hash": "hashed_password",
  "is_active": true
}
```

- Backend automatically generates `user_id`
- Inserts version `1`

---

### 5.2 Get Current User (GET)

```http
GET /api/v1/users/{user_id}
```

- Returns **only active version** (`effective_end_dt IS NULL`)

---

### 5.3 Get User History (SCD‑2)

```http
GET /api/v1/users/{user_id}/history
```

- Returns **all versions** ordered by `version_no`
- Includes historical (expired) rows

---

### 5.4 Update User (SCD‑2 Update)

```http
PUT /api/v1/users/{user_id}
Content-Type: application/json
```

**Request Body (partial update supported):**
```json
{
  "full_name": "John Doe Updated",
  "phone": "9999999999",
  "is_active": false
}
```

**Behavior:**
- Expires current row (`effective_end_dt` set)
- Inserts new row
- Increments `version_no`
- Preserves history

---

## 6. SCD Type‑2 Summary

- `user_id` → Business key (constant across versions)
- `id` → Surrogate primary key
- `version_no` → Incremented on every update
- `effective_end_dt IS NULL` → Current active record

This design ensures:
- Full audit history
- No destructive updates
- Safe, scalable data modeling

---

## 7. Notes & Best Practices

- Use **partial unique indexes** for SCD‑2 uniqueness (e.g., email)
- Do not use generic CRUD for versioned tables
- Always query SCD tables via **business keys**

---

✅ Project is now ready for GitHub check‑in and collaboration.


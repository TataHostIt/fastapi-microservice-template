# File & Structure Rules

Apply these rules when creating new files, growing existing ones, or refactoring modules.

---

## 1. The 300-Line Limit

**No file in this repository may exceed 300 lines** (including blank lines and comments).

This is a hard limit, not a guideline. If completing a task would push any file past 300 lines, split the file **as part of the same task** — never leave an oversized file behind.

---

## 2. How to Split Files

When a file approaches the limit, split it by the natural seam closest to the boundary.

### Router files — split by sub-resource or action group

```
# BEFORE: app/routers/users.py (350 lines — too large)

# AFTER: split by action type
app/routers/
├── users_read.py     # GET /users, GET /users/{id}
└── users_write.py    # POST /users, PUT /users/{id}, DELETE /users/{id}
```

### Model/schema files — split by domain object

```
# BEFORE: app/models.py (400 lines — too large)

# AFTER: split by domain
app/schemas/
├── __init__.py
├── users.py          # UserResponse, CreateUserRequest, UpdateUserRequest
└── orders.py         # OrderResponse, CreateOrderRequest
```

### Service/logic files — split by responsibility

```
# BEFORE: app/services/inventory.py (380 lines — too large)

# AFTER: split by concern
app/services/
├── inventory_fetch.py    # read operations
└── inventory_mutate.py   # create/update/delete operations
```

### Test files — split by endpoint group

```
# BEFORE: tests/routers/test_users.py (320 lines — too large)

# AFTER: split by action type
tests/routers/
├── test_users_get.py
└── test_users_post.py
```

---

## 3. Update Imports After Splitting

After splitting a file, update every import statement in the codebase that referenced the old path. Use grep to find all references:

```bash
grep -r "from app.routers.users import" .
grep -r "from app.models import" .
```

Update each one to point to the new location.

---

## 4. Project Directory Layout

Maintain this top-level structure. New files go in the most specific existing directory:

```
.
├── app/
│   ├── __init__.py          # Version + project ID
│   ├── gunicorn_config.py   # Gunicorn worker config
│   ├── health.py            # HealthcheckResponse model
│   ├── logger.py            # StructuredLogger
│   ├── main.py              # App factory, middleware, router registration
│   ├── schemas/             # Pydantic models (create when app/models.py > 150 lines)
│   ├── services/            # Business logic (create when routers start holding logic)
│   └── routers/             # One file per domain
├── tests/
│   ├── conftest.py          # Shared fixtures
│   └── routers/             # Mirror of app/routers/
├── rules/                   # Coding rule files (this directory)
├── helm/                    # Kubernetes Helm values
├── .github/workflows/       # CI pipelines
├── Dockerfile
├── start.sh                 # Production entrypoint (Gunicorn)
├── localstart.sh            # Dev entrypoint (Uvicorn --reload)
├── requirements.txt         # Runtime dependencies
├── CLAUDE.md                # AI assistant rules index
└── README.md
```

---

## 5. When to Create New Files

Create a new file when — and only when — one of these is true:

1. An existing file would exceed 300 lines with the new code
2. The new code is a clearly separate domain (new router, new schema group, new service)
3. The file is explicitly required by the framework (e.g., `conftest.py`, `__init__.py`)

Do not create helper files, utility modules, or base classes speculatively. Write the logic where it is needed first; extract only when there is genuine reuse across multiple call sites.

---

## 6. `__init__.py` Files

Every new package directory must include an `__init__.py`. Keep it empty unless there is a specific re-export needed by callers.

---

## 7. Tracking Line Counts

Before finishing any task that touches a Python file, check its line count:

```bash
wc -l app/routers/users.py
```

If the count is over 300, split before marking the task done.

# Python Coding Rules

Apply these rules to every `.py` file in this repository.

---

## 1. Type Hints — Mandatory

Every function parameter and return value must have a type annotation. No exceptions.

```python
# CORRECT
def get_user(user_id: int) -> UserResponse:
    ...

# WRONG — missing type annotations
def get_user(user_id):
    ...
```

Use `Optional[X]` (or `X | None` in Python 3.10+) for nullable values. Never use `Any` unless interfacing with an untyped third-party library, and add a comment explaining why.

---

## 2. Docstrings — Mandatory on Every Function

Every function — including private helpers, class methods, and router handlers — must have a **Google-style docstring** with:

- A one-line summary on the first line
- A blank line, then `Args:`, `Returns:`, and `Raises:` sections as applicable

```python
def healthcheck() -> HealthcheckResponse:
    """Return the current health status of the service.

    Args:
        None

    Returns:
        HealthcheckResponse: Contains the status message, API version string,
            and current UTC timestamp.
    """
```

```python
async def add_process_time_header(request: Request, call_next: Callable) -> Any:
    """Middleware that records and appends request processing duration.

    Args:
        request (Request): The incoming FastAPI/Starlette request object.
        call_next (Callable): The next handler in the middleware chain.

    Returns:
        Response: The original response with an added 'X-Process-Time' header
            containing elapsed time in seconds as a float string.
    """
```

If a function can raise an exception callers should handle:

```python
def fetch_record(record_id: int) -> Record:
    """Fetch a single record by ID from the database.

    Args:
        record_id (int): The unique identifier of the record.

    Returns:
        Record: The matching record object.

    Raises:
        HTTPException: 404 if no record with the given ID exists.
    """
```

---

## 3. Naming Conventions

| Construct | Convention | Example |
|-----------|------------|---------|
| Functions and methods | `snake_case` | `get_health_status()` |
| Variables | `snake_case` | `pod_name`, `process_time` |
| Classes | `PascalCase` | `HealthcheckResponse`, `LogEncoder` |
| Constants / module-level env reads | `UPPER_SNAKE_CASE` | `PROFILE`, `DATABASE_URL` |
| Pydantic response models | `PascalCase` + `Response` suffix | `UserResponse` |
| Pydantic request body models | `PascalCase` + `Request` suffix | `CreateUserRequest` |
| Router files | `snake_case.py` | `health.py`, `user_profile.py` |
| Test files | `test_<module>.py` | `test_health.py` |

---

## 4. Import Order

Strictly follow PEP 8 — three groups separated by blank lines:

```python
# 1. Standard library
import os
import time
from typing import Any, Callable

# 2. Third-party
from fastapi import APIRouter, Request
from pydantic import BaseModel

# 3. Internal (app.*)
from app import __version__
from app.health import HealthcheckResponse
from app.logger import logger
```

Never mix groups. Never use wildcard imports (`from module import *`).

---

## 5. Environment Variables

Read all environment variables at **module level** using `os.getenv()` with a safe default. Never hard-code secrets or environment-specific values inline.

```python
# CORRECT — module-level, safe default
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./local.db")
LOG_LEVEL = os.getenv("LOG_LEVEL", "DEBUG")

# WRONG — hard-coded
DATABASE_URL = "postgresql://prod-host:5432/mydb"
```

---

## 6. Exception Handling

Always catch specific exceptions. Never use bare `except:` or silent `except Exception: pass`.

```python
# CORRECT
try:
    result = call_external_service()
except httpx.TimeoutException as exc:
    logger.error(f"Service call timed out: {exc}")
    raise HTTPException(status_code=504, detail="Upstream timeout")

# WRONG — swallows all errors silently
try:
    result = call_external_service()
except:
    pass
```

---

## 7. Pydantic Models

- Use `StrictStr`, `StrictInt`, etc. from `pydantic.types` where type coercion would hide bugs.
- Place all models in `app/models.py` or `app/schemas/` — never inside router files.
- Add `model_config = ConfigDict(from_attributes=True)` when reading from ORM objects.

```python
from pydantic import BaseModel
from pydantic.types import StrictStr
from datetime import datetime

class HealthcheckResponse(BaseModel):
    message: StrictStr
    version: StrictStr
    time: datetime
```

---

## 8. What to Avoid

- No `print()` — use the structured logger
- No unused imports — remove them
- No commented-out code — delete it or track it in git
- No speculative abstractions — only build what the current task requires
- No backwards-compatibility shims for removed code

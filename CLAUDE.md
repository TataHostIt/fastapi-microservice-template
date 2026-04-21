# CLAUDE.md

This file governs how Claude Code works in this repository. Rules are split into focused files — read the relevant one before making changes.

## Rules Index

| Topic | File | When to read |
|-------|------|--------------|
| Python standards | [rules/python.md](rules/python.md) | Any `.py` file change |
| FastAPI routers | [rules/routers.md](rules/routers.md) | Any file in `app/routers/` |
| Testing | [rules/testing.md](rules/testing.md) | Any file in `tests/` |
| Logging | [rules/logging.md](rules/logging.md) | Using `logger` anywhere |
| File & structure | [rules/file-structure.md](rules/file-structure.md) | Creating or growing any file |

## Non-Negotiable Constraints

- **All files must stay under 300 lines.** If a file grows beyond that, split it before finishing the task. See [rules/file-structure.md](rules/file-structure.md).
- **Every function must have a docstring** with Args, Returns, and Raises. See [rules/python.md](rules/python.md).
- **Every router endpoint must have a test.** See [rules/testing.md](rules/testing.md).
- **Never use `print()` or bare `logging.getLogger()`** — always use `from app.logger import logger`.

## Project Overview

Production FastAPI microservice template — Python 3.11, Gunicorn + Uvicorn workers, structured JSON logging, Docker, Kubernetes/Helm. When deriving a new service, globally replace `fastapi-microservice-template` with the new service name.

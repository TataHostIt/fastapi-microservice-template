# Testing Rules

Apply these rules to every file under `tests/` and when adding new endpoints or logic.

---

## 1. Test Location and Structure

Tests mirror the `app/` source structure:

```
tests/
├── __init__.py
├── conftest.py              # Shared fixtures: TestClient, env var overrides
└── routers/
    ├── __init__.py
    ├── test_health.py       # Tests for app/routers/health.py
    └── test_test.py         # Tests for app/routers/test.py
```

As the service grows, add subdirectories matching new `app/` modules (e.g., `tests/services/`, `tests/schemas/`).

---

## 2. Test Client Setup

Use `TestClient` from FastAPI. Place the shared client in `tests/conftest.py` so every test module can import it without repetition.

```python
# tests/conftest.py
import pytest
from fastapi.testclient import TestClient
from app.main import api


@pytest.fixture(scope="module")
def client() -> TestClient:
    """Provide a TestClient instance scoped to the test module.

    Args:
        None

    Returns:
        TestClient: A configured test client for the FastAPI app.
    """
    return TestClient(api)
```

Install test dependencies:

```bash
pip install pytest httpx
```

Or add them to `requirements-dev.txt`:

```
pytest>=8.0.0
httpx>=0.27.0
```

---

## 3. Every Endpoint Must Have Tests

For each route, write tests covering all three categories:

| Category | What to test |
|----------|-------------|
| Happy path | Nominal input → expected 2xx status + response body shape |
| Error cases | Invalid/missing input → expected 4xx/5xx + error detail |
| Edge cases | Boundary values, empty strings, missing env vars |

---

## 4. Test Naming Pattern

```
test_{resource_or_unit}_{scenario}_{expected_outcome}
```

Examples:
- `test_healthcheck_returns_200`
- `test_healthcheck_body_contains_required_fields`
- `test_get_item_invalid_id_returns_422`
- `test_test_endpoint_renders_html_with_pod_name`

---

## 5. Real Test Examples

```python
# tests/routers/test_health.py
from fastapi.testclient import TestClient
from app.main import api

client = TestClient(api)


def test_healthcheck_returns_200():
    """Happy path: healthcheck returns HTTP 200.

    Args:
        None

    Returns:
        None
    """
    response = client.get("/fastapi-microservice-template/healthcheck")
    assert response.status_code == 200


def test_healthcheck_body_contains_required_fields():
    """Response body includes message, version, and time fields.

    Args:
        None

    Returns:
        None
    """
    response = client.get("/fastapi-microservice-template/healthcheck")
    body = response.json()
    assert "message" in body
    assert "version" in body
    assert "time" in body


def test_healthcheck_message_value():
    """Message field contains the expected status string.

    Args:
        None

    Returns:
        None
    """
    response = client.get("/fastapi-microservice-template/healthcheck")
    assert response.json()["message"] == "Application is running"
```

```python
# tests/routers/test_test.py
from fastapi.testclient import TestClient
from app.main import api

client = TestClient(api)


def test_test_endpoint_returns_200():
    """Happy path: test endpoint returns HTTP 200.

    Args:
        None

    Returns:
        None
    """
    response = client.get("/fastapi-microservice-template/test")
    assert response.status_code == 200


def test_test_endpoint_returns_html():
    """Response content-type is text/html.

    Args:
        None

    Returns:
        None
    """
    response = client.get("/fastapi-microservice-template/test")
    assert "text/html" in response.headers["content-type"]


def test_test_endpoint_shows_pod_name(monkeypatch):
    """HOSTNAME env var value appears in the rendered HTML.

    Args:
        monkeypatch: pytest monkeypatch fixture for env var injection.

    Returns:
        None
    """
    monkeypatch.setenv("HOSTNAME", "test-pod-abc123")
    response = client.get("/fastapi-microservice-template/test")
    assert "test-pod-abc123" in response.text


def test_test_endpoint_unknown_hostname(monkeypatch):
    """Falls back to 'Unknown' when HOSTNAME is not set.

    Args:
        monkeypatch: pytest monkeypatch fixture for env var injection.

    Returns:
        None
    """
    monkeypatch.delenv("HOSTNAME", raising=False)
    response = client.get("/fastapi-microservice-template/test")
    assert "Unknown" in response.text
```

---

## 6. No Global State Between Tests

Use `monkeypatch` to set or delete environment variables. Never modify `os.environ` directly without restoring it — monkeypatch handles cleanup automatically.

```python
# CORRECT — monkeypatch restores env state after the test
def test_something_with_env(monkeypatch):
    monkeypatch.setenv("MY_VAR", "test-value")
    ...

# WRONG — leaks state into subsequent tests
def test_something_with_env():
    os.environ["MY_VAR"] = "test-value"
    ...
```

---

## 7. Run Tests

```bash
# Run all tests
pytest tests/ -v

# Run a specific file
pytest tests/routers/test_health.py -v

# Run with coverage (requires pytest-cov)
pytest tests/ --cov=app --cov-report=term-missing
```

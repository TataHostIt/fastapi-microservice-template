# FastAPI Microservice Template

![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.128.0+-009688.svg)
![Docker](https://img.shields.io/badge/Docker-Enabled-2496ED.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

A production-ready, Dockerized boilerplate for building Python microservices with FastAPI. Includes structured JSON logging, Gunicorn/Uvicorn configuration, health check endpoints, and a deployment verification UI — so you can go from template to running service with minimal ceremony.

---

## Features

- **Python 3.11** with full type hints throughout
- **Production server** — Gunicorn process manager with Uvicorn async workers
- **Structured logging** — JSON-formatted logs with color support for local dev
- **Health checks** — `/healthcheck` endpoint ready for Kubernetes liveness/readiness probes
- **Deployment test UI** — HTML endpoint that displays the serving Pod ID to verify Ingress routing
- **Docker-ready** — optimized multi-layer `Dockerfile` with non-root best practices
- **Kubernetes/Helm** — Helm values file included for `dev` environment deployments
- **CI pipeline** — GitHub Actions workflow wired to a reusable build-and-deploy pipeline

---

## Project Structure

```text
.
├── app/
│   ├── __init__.py            # Version and project ID from env vars
│   ├── gunicorn_config.py     # Worker count, timeout, bind config
│   ├── health.py              # HealthcheckResponse Pydantic model
│   ├── logger.py              # StructuredLogger with JSON + color support
│   ├── main.py                # FastAPI app, CORS middleware, router registration
│   └── routers/
│       ├── health.py          # GET /healthcheck
│       └── test.py            # GET /test — HTML deployment verification UI
├── tests/                     # (add your tests here — see Testing section)
├── helm/
│   └── dev-values.yaml        # Helm values for dev environment
├── .github/
│   └── workflows/
│       └── ci-dev.yaml        # CI: build + deploy to dev on push to main
├── Dockerfile                 # Python 3.11-slim production image
├── start.sh                   # Entrypoint for Docker/Kubernetes (Gunicorn)
├── localstart.sh              # Local dev entrypoint (Uvicorn with --reload)
├── requirements.txt           # Runtime dependencies
├── CLAUDE.md                  # AI assistant coding rules for this repo
└── LICENCE
```

---

## Quickstart

### Prerequisites

- Python 3.11+
- Docker (optional, for container builds)

### Local Development

```bash
# 1. Clone the repo
git clone https://github.com/TataHostIt/fastapi-microservice-template.git
cd fastapi-microservice-template

# 2. Create and activate a virtual environment
python3.11 -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Start the development server (hot-reload enabled)
chmod +x localstart.sh
./localstart.sh
```

The API is available at **http://localhost:8080**

| URL | Description |
|-----|-------------|
| `GET /fastapi-microservice-template/healthcheck` | Health check — returns version + timestamp |
| `GET /fastapi-microservice-template/test` | HTML page showing the serving Pod/Container ID |
| `GET /docs` | Interactive Swagger UI |
| `GET /redoc` | ReDoc API documentation |

### Running with Docker

```bash
# Build
docker build -t fastapi-microservice-template:latest .

# Run
docker run -p 8080:8080 fastapi-microservice-template:latest
```

---

## API Reference

### `GET /fastapi-microservice-template/healthcheck`

Returns the operational status of the service.

**Response `200 OK`**
```json
{
  "message": "Application is running",
  "version": "1.0.0",
  "time": "2024-01-15T12:34:56.789000"
}
```

### `GET /fastapi-microservice-template/test`

Returns an HTML page confirming the deployment is reachable and displaying the Pod/Container hostname. Useful for verifying Kubernetes Ingress routing after a deploy.

---

## Configuration

All runtime configuration is read from environment variables. Set these in your shell, a `.env` file (local dev), or Kubernetes ConfigMaps/Secrets.

| Variable | Default | Description |
|----------|---------|-------------|
| `PORT` | `8080` | Port Gunicorn binds to |
| `API_TAG_VERSION` | `1.0.0` | Version string returned in health check responses |
| `PROJECT_ID` | `local` | Logical project/environment identifier |
| `LOG_LEVEL` | `DEBUG` | Logging level (`DEBUG`, `INFO`, `WARNING`, `ERROR`) |
| `PROFILE` | `dv` | When set to `pr-disabled`, switches to full JSON structured logging |

### Gunicorn Tuning

Edit `app/gunicorn_config.py` to adjust:

```python
threads  = 12    # threads per worker
workers  = 2     # number of worker processes
timeout  = 3000  # request timeout in seconds
```

A common starting point for production is `workers = (2 * CPU_cores) + 1`.

---

## Testing

Install test dependencies:

```bash
pip install pytest httpx
```

Run the test suite:

```bash
pytest tests/ -v
```

### Writing Tests

Tests live in `tests/` and mirror the `app/` structure. Use `TestClient` from FastAPI:

```python
# tests/routers/test_health.py
from fastapi.testclient import TestClient
from app.main import api

client = TestClient(api)


def test_healthcheck_returns_200():
    """Happy path: healthcheck returns HTTP 200 with required fields."""
    response = client.get("/fastapi-microservice-template/healthcheck")
    assert response.status_code == 200
    body = response.json()
    assert "message" in body
    assert "version" in body
    assert "time" in body


def test_test_endpoint_renders_html(monkeypatch):
    """Test endpoint returns HTML with the Pod hostname."""
    monkeypatch.setenv("HOSTNAME", "test-pod-xyz")
    response = client.get("/fastapi-microservice-template/test")
    assert response.status_code == 200
    assert "test-pod-xyz" in response.text
```

See [CLAUDE.md](./CLAUDE.md) for the full testing conventions used in this repo.

---

## Creating a New Service from This Template

### 1. Clone and rename

```bash
git clone https://github.com/TataHostIt/fastapi-microservice-template.git inventory-service
cd inventory-service
```

### 2. Reset git history (recommended)

```bash
rm -rf .git
git init
git add .
git commit -m "chore: initial commit from fastapi-microservice-template"
```

### 3. Replace all template references

Run a global **Find & Replace** across the entire project:

- Find: `fastapi-microservice-template`
- Replace: `inventory-service` (your new service name)

Files to update: `app/routers/health.py`, `app/routers/test.py`, `localstart.sh`, `start.sh`, `.github/workflows/ci-dev.yaml`, `helm/dev-values.yaml`, and this `README.md`.

### 4. Update the README title and description

Replace the title and the description paragraph at the top of this file to describe your specific service.

### 5. Add your business logic

- Add new router files under `app/routers/`
- Add Pydantic models to `app/models.py` (create it)
- Register new routers in `app/main.py`
- Add tests under `tests/routers/`

---

## CI / CD

On every push to `main`, the GitHub Actions workflow in `.github/workflows/ci-dev.yaml` triggers a reusable pipeline that:

1. Builds the Docker image
2. Pushes it to the container registry
3. Deploys to the `dev` Kubernetes environment using the Helm values in `helm/dev-values.yaml`

To adapt this for your service, update `app_name` in the workflow file.

---

## Contributing

Contributions are welcome. Please follow these steps:

1. Fork the repository
2. Create a feature branch: `git checkout -b feat/my-improvement`
3. Make your changes following the conventions in [CLAUDE.md](./CLAUDE.md)
4. Add or update tests in `tests/`
5. Run `pytest tests/ -v` and confirm all tests pass
6. Open a pull request with a clear description of what you changed and why

Please keep pull requests focused — one concern per PR.

---

## License

[MIT](./LICENCE)

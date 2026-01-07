# FastAPI Microservice Template

![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.128.0+-009688.svg)
![Docker](https://img.shields.io/badge/Docker-Enabled-2496ED.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

A production-ready, Dockerized boilerplate for building high-performance Python microservices. This repository serves as a foundational template featuring structured logging, Gunicorn/Uvicorn configuration, health checks, and a pipeline testing UI.

## ⚡ Features

* **Python 3.11**: Leverages the latest performance improvements.
* **Production Server**: Configured with `gunicorn` as the process manager and `uvicorn` workers.
* **Docker Ready**: Optimized `Dockerfile` with non-root user best practices and caching.
* **Health Checks**: Built-in endpoints for liveness/readiness probes.
* **Pipeline Test UI**: A visual HTML endpoint to verify Ingress/Deployment success immediately.
* **Modular Structure**: Clean separation of routers, logic, and configuration.

## 📂 Project Structure

```text
.
├── app
│   ├── __init__.py
│   ├── gunicorn_config.py   # Production Gunicorn configuration
│   ├── health.py            # Health check logic
│   ├── logger.py            # JSON structured logging
│   ├── main.py              # App entry point
│   └── routers
│       ├── health.py        # API routes for health
│       └── test.py          # Visual UI for testing Ingress
├── Dockerfile               # Python 3.11 Slim Docker build
├── localstart.sh            # Script for local development
├── start.sh                 # Entrypoint for Docker/K8s
└── requirements.txt         # Python dependencies

```

## 🛠 Creating a New Service

Follow these steps to turn this template into a new microservice:

### 1. Clone & Rename

Clone the repository and rename the directory to your new service name (e.g., `inventory-service`).

```bash
git clone [https://github.com/TataHostIt/fastapi-microservice-template.git](https://github.com/TataHostIt/fastapi-microservice-template.git) inventory-service
cd inventory-service

```

### 2. Reset Git History

*(Optional but recommended)* Remove the template's history to start fresh.

```bash
rm -rf .git
git init
git add .
git commit -m "Initial commit from template"

```

### 3. Search & Replace (Crucial)

To ensure all naming conventions match your new project, perform a global **Search and Replace** in your IDE (VS Code, PyCharm, etc.) across the entire project directory.

* **Find:** `fastapi-microservice-template`
* **Replace with:** `inventory-service` (or your new project name)

### 4. Update Documentation

Open this `README.md` file and:

1. Change the **Title** (at the top) to your new service name.
2. Update the **Description** to explain what this specific microservice does.

---

## 🚀 Getting Started

### Local Development

It is recommended to use a virtual environment.

```bash
# Create and activate venv
python3.11 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the local start script
chmod +x localstart.sh
./localstart.sh

```

*The app will be available at http://localhost:8080*

### Running with Docker

```bash
# Build the image
docker build -t my-app:latest .

# Run the container
docker run -p 8080:8080 my-app:latest

```

## 🧪 Testing the Deployment

This template includes a specific route designed to test Kubernetes Ingress and Pod identity.

* **Endpoint:** `/pipeline-test-app/test`
* **Method:** `GET`
* **Response:** An HTML page displaying the serving Pod ID.

This allows you to visually confirm that traffic is routing correctly through your Load Balancer/Ingress Controller.

## ⚙️ Configuration

* **Environment Variables**: The application is designed to read configuration from environment variables (Kubernetes Secrets/ConfigMaps).
* **Gunicorn**: Settings such as worker count and timeouts can be adjusted in `app/gunicorn_config.py`.
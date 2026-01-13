#!/bin/sh

echo "Starting fastapi-microservice-template..."

echo "Starting fastapi-microservice-template..."
uvicorn app.main:api --host 0.0.0.0 --port 8080 --reload

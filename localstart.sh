#!/bin/sh

echo "Starting pipeline-test-app..."

echo "Starting pipeline-test-app..."
uvicorn app.main:api --host 0.0.0.0 --port 8080 --reload

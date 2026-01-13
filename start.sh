#!/bin/bash

#
# /etc/config/env is created in initContainers which is defined in heml value file
#
#if [ -f /etc/config/env ]; then
#    while IFS= read -r line || [[ -n "$line" ]]; do
#        export $line
#    done < /etc/config/env
#fi
# Kubernetes env vars from values-dv.yaml take precedence - commenting out hardcoded secrets
echo "Starting fastapi-microservice-template..."

gunicorn app.main:api -c app/gunicorn_config.py
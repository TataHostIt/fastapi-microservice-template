"""gunicorn server configuration."""
import os

threads = 12
workers = 2
timeout = 3000
bind = f":{os.environ.get('PORT', '8080')}"
worker_class = "uvicorn.workers.UvicornWorker"

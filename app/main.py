import os
import time
import logging
from typing import Any, Callable

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from app import __project_id__, __version__
from app.routers import health, test
os.environ["TZ"] = "UTC"
logger = logging.getLogger("uvicorn.error")

#
#   create the api
#
api = FastAPI(title=f"fastapi-microservice-template: {__project_id__}", version=__version__)
api.add_middleware(
    CORSMiddleware,
    allow_origins='*',
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#
#   middleware
#
@api.middleware("http")
async def add_process_time_header(request: Request, call_next: Callable) -> Any:
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


#
#   set routers
#
api.include_router(health.router)
api.include_router(test.router)
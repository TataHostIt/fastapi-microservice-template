from datetime import datetime

from fastapi import APIRouter

from app import __version__
from app.health import HealthcheckResponse

router = APIRouter()


@router.get("/fastapi-microservice-template/healthcheck", response_model=HealthcheckResponse, tags=["health"])
def healthcheck() -> HealthcheckResponse:
    message = "Application is running"
    return HealthcheckResponse(
        message=message, version=__version__, time=datetime.now()
    )

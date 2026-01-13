import os

from fastapi import APIRouter
from fastapi.responses import HTMLResponse

from app.logger import logger

router = APIRouter()


@router.get("/fastapi-microservice-template/test", tags=["test"], response_class=HTMLResponse)
def hello():
    pod_name = os.getenv('HOSTNAME', 'Unknown')
    logger.info(f"Get Request for test, podname: {pod_name}")
    return f""" <html> <head> <title>Deployment Test UI</title> <style> body {{ font-family: sans-serif; text-align: 
    center; padding-top: 50px; background-color: #f0f2f5; }} .container {{ background: white; padding: 40px; 
    border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); display: inline-block; }} h1 {{ color: #2c3e50; }} 
    .status {{ color: #27ae60; font-weight: bold; }} </style> </head> <body> <div class="container"> <h1>🚀 Pipeline 
    Test App</h1> <p>If you can see this, the Ingress is working!</p> <hr> <p>Served by Pod/Container ID: <span 
    class="status">{pod_name}</span></p>
            </div>
        </body>
    </html>
    """

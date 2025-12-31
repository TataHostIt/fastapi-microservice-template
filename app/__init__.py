"""pipeline-test-app"""
import os

__version__ = os.getenv("API_TAG_VERSION", "1.0.0")
__project_id__ = os.getenv("PROJECT_ID", "local")
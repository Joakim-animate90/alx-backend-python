from datetime import datetime
import logging
import os

# Configure logging to file
logging.basicConfig(
    filename=os.path.join(os.path.dirname(os.path.dirname(__file__)), 'requests.log'),
    level=logging.INFO,
    format='%(message)s'
)
logger = logging.getLogger(__name__)

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Log the request details
        user = request.user if hasattr(request, 'user') else 'Anonymous'
        logger.info(f"{datetime.now()} - User: {user} - Path: {request.path}")

        response = self.get_response(request)
        return response

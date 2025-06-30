from datetime import datetime, time
import logging
import os
from django.http import HttpResponseForbidden

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


class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        current_time = datetime.now().time()
        # Restrict access between 9PM (21:00) and 6AM (06:00)
        if time(21, 0) <= current_time or current_time <= time(6, 0):
            return HttpResponseForbidden("Access denied: Service unavailable during these hours (9PM-6AM)")
        
        return self.get_response(request)

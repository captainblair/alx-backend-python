# chats/middleware.py
import logging
from datetime import datetime

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        # Django passes in get_response which we call later
        self.get_response = get_response
        # Set up logger (writes to requests.log)
        logging.basicConfig(
            filename="requests.log",   # log file in project root
            level=logging.INFO,        # log level
            format="%(message)s"       # only log message, no extras
        )

    def __call__(self, request):
        # Get user info (Anonymous if not logged in)
        user = request.user if request.user.is_authenticated else "Anonymous"

        # Log details: timestamp - user - path
        logging.info(f"{datetime.now()} - User: {user} - Path: {request.path}")

        # Continue with normal request-response cycle
        response = self.get_response(request)
        return response

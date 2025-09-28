from datetime import datetime
from django.conf import settings

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Determine user; fallback if not authenticated
        user = request.user if request.user.is_authenticated else "Anonymous"
        log_path = settings.BASE_DIR / "requests.log"

        # Append log
        with open(log_path, "a") as f:
            f.write(f"{datetime.now()} - User: {user} - Path: {request.path}\n")

        response = self.get_response(request)
        return response

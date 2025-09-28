# chats/middleware.py
from datetime import datetime
from django.http import HttpResponseForbidden

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        with open('requests.log', 'a') as f:
            f.write(f"Requested path: {request.path} at {datetime.now()}\n")
        response = self.get_response(request)
        return response


class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        current_hour = datetime.now().hour
        # Deny access outside 6AM - 9PM
        if current_hour < 6 or current_hour >= 21:
            return HttpResponseForbidden("Access denied: Outside allowed hours (6AM-9PM)")
        response = self.get_response(request)
        return response

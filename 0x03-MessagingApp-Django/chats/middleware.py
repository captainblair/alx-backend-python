# chats/middleware.py
from datetime import datetime
from django.http import HttpResponseForbidden

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Make sure requests.log exists and write one line
        with open("requests.log", "a") as f:
            f.write(f"{datetime.now()}: {request.method} {request.path}\n")
        response = self.get_response(request)
        return response

class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        current_hour = datetime.now().hour
        # deny access if current hour is outside 18-21 (6PM-9PM)
        if current_hour < 18 or current_hour > 21:
            return HttpResponseForbidden("Chat is available only between 6PM and 9PM")
        response = self.get_response(request)
        return response

# chats/middleware.py
from django.http import HttpResponseForbidden
from datetime import datetime

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        with open('requests.log', 'a') as f:
            f.write(f"{datetime.now()}: {request.method} {request.path}\n")
        return self.get_response(request)

class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        current_hour = datetime.now().hour
        # deny access if current hour is before 18 (6PM) or after 21 (9PM)
        if current_hour < 18 or current_hour > 21:
            return HttpResponseForbidden("Chat is available only between 6PM and 9PM")
        return self.get_response(request)

# chats/middleware.py
from datetime import datetime
from django.http import HttpResponseForbidden

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else "Anonymous"
        with open("requests.log", "a") as f:
            f.write(f"{datetime.now()} - User: {user} - Path: {request.path}\n")
        response = self.get_response(request)
        return response

class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        current_hour = datetime.now().hour
        # Allow access only between 6 AM (6) and 9 PM (21)
        if not (6 <= current_hour <= 21):
            return HttpResponseForbidden("Access to chat is restricted during these hours.")
        return self.get_response(request)

# chats/middleware.py

class RequestLoggingMiddleware:
    """Middleware that logs every request to requests.log"""

    def __init__(self, get_response):
        self.get_response = get_response  # Django standard

    def __call__(self, request):
        # Append the requested path to requests.log
        with open("requests.log", "a") as f:
            f.write(f"{request.path}\n")

        response = self.get_response(request)  # continue processing
        return response


class RestrictAccessByTimeMiddleware:
    """Middleware that blocks access outside 9am-5pm"""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        import datetime
        now = datetime.datetime.now()
        if not (9 <= now.hour < 17):
            from django.http import HttpResponse
            return HttpResponse("Access not allowed at this time.", status=403)
        return self.get_response(request)

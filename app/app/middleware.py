import json

from django.http import JsonResponse

class TestMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ding = json.loads(request.body).get("ding")
        if not ding or ding != "dong":
            return JsonResponse({"message": "sorry, we are sleeping now"})

        response = self.get_response(request)
        return response


class TestMiddleware2:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        return JsonResponse({"status": "error", "message": repr(exception)}, status=500)
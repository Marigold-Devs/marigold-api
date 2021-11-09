import json
import sys

from django.http import HttpResponsePermanentRedirect
from backend.web_requests import models as web_requests_models


def dumps(value):
    return json.dumps(value, default=lambda o: None)


class WebRequestMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        request_body = request.body.decode("utf-8")

        response = self.get_response(request)

        if request.method == "GET":
            # no need to log GET requests
            return response
        if response.status_code != 200 and response.status_code != 204:
            # no need to log failed requests
            return response
        if "/tokens" in request.path or "/web_requests" in request.path:
            return response

        try:
            web_requests_models.WebRequest(
                host=request.get_host(),
                path=request.path,
                method=request.method,
                uri=request.build_absolute_uri(),
                status_code=response.status_code,
                get=None if not request.GET else dumps(request.GET),
                post=None if not request_body else dumps(request_body),
            ).save()

        except Exception as e:
            print(sys.stderr, "Error saving request log", e)

        return response

"""
Implementation of exception handlers for the API.
"""
from rest_framework.response import Response
from rest_framework.views import exception_handler

from backend.generic.serializers.response import ErrorResponseSerializer
from backend.utils.errors import simplify_errors


def api_exception_handler(exc, context):
    """API Exception Handler

    Default (and basic) exception handler.
    """
    old_response = exception_handler(exc, context)

    if old_response is None:
        return old_response

    error = simplify_errors(old_response.data)

    response = Response(
        ErrorResponseSerializer({"error": error}).data, old_response.status_code
    )

    return response

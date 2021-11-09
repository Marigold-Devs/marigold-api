"""
Generic Response Serializers for the entirety of the API, either to be used
or extended.
"""
from rest_framework import serializers

### File Specific Pylint Configuration ###
# pylint: disable=abstract-method


class ErrorResponseSerializer(serializers.Serializer):
    """Response Error Serializer

    Serializer to keep error information uniform.
    """

    error = serializers.CharField()

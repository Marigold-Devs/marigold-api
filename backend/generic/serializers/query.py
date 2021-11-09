"""
Generic Query Serializers for the entirety of the API, either to be used or
extended.
"""
from rest_framework import serializers

### File Specific Pylint Configuration ###
# pylint: disable=abstract-method


class FieldsQuerySerializer(serializers.Serializer):
    """Fields Query Serializer

    Generic serializer to query parameters for fields. All query
    serializers should extend from this.
    """

    fields = serializers.CharField(required=False)

    def validate(self, attrs):
        """Validate

        When `.is_valid()` is called, this parses valid fields. This only
        parses `fields` or keys that end with `__fields`.
        """
        for key, item in attrs.items():
            if key == "fields" or key.endswith("__fields"):
                attrs[key] = item.split(",")

        return attrs

"""
Class implementations of generic fields meant to be used through
out EJJY for DRYness and maintainability.
"""
from django.db import models
from rest_framework import serializers


class ModelIdQueryField(serializers.IntegerField):
    """Model Id Query Serializer

    This is only for write-only fields.
    """

    def __init__(self, *args, **kwargs):
        """
        Adds additional parameters `query` and `queryset`.

        Args:
            query (bool): Whether this model should be queried during validation
                or not.
            queryset (QuerySet): QuerySet to use when model is queried during
                validation. If `query` is `False`, then `queryset` is not used.
        """
        query = kwargs.pop("query", False)
        queryset = kwargs.pop("queryset", None)

        super().__init__(*args, **kwargs)

        self.query = query
        self.queryset = queryset


def NON_POLYMORPHIC_CASCADE(collector, field, sub_objs, using):
    return models.CASCADE(collector, field, sub_objs.non_polymorphic(), using)

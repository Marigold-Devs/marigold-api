"""
Generic implementation for viewsets.
"""
from rest_framework import viewsets
from rest_framework.response import Response

from backend.generic.serializers import query as query_serializers


class BaseViewSet(viewsets.GenericViewSet):
    """Generic Optional Fields Viewset

    Generic Viewset that automatically parses query parameters for `fields`
    that inidicate which fields the requestor wants. Each `fields`
    parameter consists of a list of comma separated field names from the
    ViewSet's serializer class.

    Say for example we have a serializer that returns the following:
    ```
    {
        "id": <int>,
        "name": <str>
        "child": {
            "id": <int>,
            "name" <str>
        },
        "datetime_create": <str>
    }
    ```
    If the requestor only requires the top level fields `id` and `name`,
    then the requestor may add `fields=id,name` to the query parameter so
    that the serializer will filter the information to:
    ```
    {
        "id": <int>,
        "name": <str>
    }
    ```
    By default, only top level fields may be filtered, which means all the
    fields under `child` cannot be filtered, only `child` itself, unless
    `field_query_serializer` is defined or `get_field_query_serializer()`
    is overriden.
    """

    extended_serializer_class = None
    field_query_serializer = None
    context_serializer_class = None

    def get_field_query_serializer(self):
        """Get Field Query Serializer Class

        Gets the class, not an instance, of `field_query_serializer`.

        Override this method in a child class if the serializer for field
        queries changes from view to view. Otherwise just set a class to
        `field_query_serializer`.
        """
        if self.field_query_serializer is None:
            return query_serializers.FieldsQuerySerializer

        return self.field_query_serializer

    def get_serializer_context(self):
        """Get Serializer Context

        Adds the optional fields to the context for use inside the viewset.

        Refer to the serializer returned by `get_field_query_serializer()`
        on what fields may be added to the context. By default, only
        `fields` is added to context if `FieldsQuerySerializer` is used.
        """
        context = super().get_serializer_context()
        fields = self.get_fields()

        if fields:
            context.update(fields)

        return context

    def get_serializer_class(self):
        """Get Serializer Class"""
        if self.action == "list_extended" or self.action == "retrieve_extended":
            return self.extended_serializer_class

        return super().get_serializer_class()

    def get_fields(self):
        """Gets Fields

        Gets the fields from the query paramaters. By default, it uses the
        serializer `FieldsQuerySerializer` while `field_query_serializer`
        is `None`.
        """
        unparsed_fields = self.request.query_params
        serializer = self.get_field_query_serializer()(data=unparsed_fields)

        if unparsed_fields and serializer.is_valid():
            return serializer.validated_data

        return None

    def list_helper(self, request, *args, **kwargs):
        context = kwargs.get("context", dict())
        queryset = kwargs.get("queryset", self.get_queryset())
        queryset = self.filter_queryset(queryset)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            serializer.context.update(context)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        serializer.context.update(context)
        return Response(serializer.data)  # pylint - disable=undefined-variable

    def retrieve_helper(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def list_helper_data_only(self, request, *args, **kwargs):
        context = kwargs.get("context", dict())
        queryset = kwargs.get("queryset", self.get_queryset())
        # queryset = self.filter_queryset(queryset)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            serializer.context.update(context)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        serializer.context.update(context)
        return Response(serializer.data)

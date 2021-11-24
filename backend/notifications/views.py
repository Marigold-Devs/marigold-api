from backend.generic.views import BaseViewSet
from backend.notifications import models as notifications_models
from backend.notifications import serializers as notifications_serializers
from drf_yasg.utils import swagger_auto_schema
from rest_framework import mixins
from rest_framework.response import Response


class NotificationsViewSet(
    BaseViewSet,
    mixins.ListModelMixin,
):
    queryset = notifications_models.Notification.objects
    serializer_class = notifications_serializers.query.NotificationsQuerySerializer

    @swagger_auto_schema(
        query_serializer=notifications_serializers.query.NotificationsQuerySerializer(),
        responses={
            200: notifications_serializers.response.NotificationResponseSerializer()
        },
    )
    def list(self, request, *args, **kwargs):
        """List Notifications

        Gets a collection of Notifications.
        """

        serializer = notifications_serializers.query.NotificationsQuerySerializer(
            data=request.query_params
        )
        serializer.is_valid(raise_exception=True)

        branch_id = serializer.validated_data.get("branch_id", None)

        queryset = self.queryset.with_branch(branch_id)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = (
                notifications_serializers.response.NotificationResponseSerializer(
                    page,
                    many=True,
                )
            )
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

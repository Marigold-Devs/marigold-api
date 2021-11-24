from backend.generic.serializers import base as generic_base
from backend.notifications import models as notifications_models
from rest_framework import serializers


class NotificationSerializer(generic_base.DynamicFieldsModelSerializer):
    class Meta:
        model = notifications_models.Notification
        fields = serializers.ALL_FIELDS

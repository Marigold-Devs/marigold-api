from backend.branches import serializers as branches_serializers
from backend.notifications import serializers as notifications_serializers
from rest_framework import serializers


class NotificationResponseSerializer(
    notifications_serializers.base.NotificationSerializer
):
    branch_product = branches_serializers.base.BranchProductProductSerializer()

    class Meta:
        model = notifications_serializers.base.NotificationSerializer.Meta.model
        fields = serializers.ALL_FIELDS
        ref_name = "NotificationResponseSerializer"

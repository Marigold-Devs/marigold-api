from rest_framework import serializers
from backend.branches import models as branches_models


class NotificationsQuerySerializer(serializers.Serializer):
    branch_id = serializers.PrimaryKeyRelatedField(
        many=False, queryset=branches_models.Branch.objects
    )

    class Meta:
        depth = 1
        fields = ["branch_id"]

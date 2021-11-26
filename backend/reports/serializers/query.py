from rest_framework import serializers
from backend.branches import models as branches_models
from backend.branches import choices as branches_choices
from backend.generic.serializers import base as generic_base


class ReportsQuerySerializer(serializers.Serializer):
    branch_id = serializers.IntegerField(required=False)

    date_range = serializers.CharField(
        default="daily",
        help_text="Choices are: <li>daily</li><li>monthly</li><li>mm/dd/yy,mm/dd/yy</li>",
    )

    class Meta:
        fields = ["branch_id", "time_range"]

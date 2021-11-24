from backend.generic.serializers import base as generic_base
from backend.deliveries import models as deliveries_models
from backend.branches import models as branches_models
from rest_framework import serializers


class DeliverySerializer(generic_base.DynamicFieldsModelSerializer):
    branch_id = serializers.PrimaryKeyRelatedField(
        many=False, queryset=branches_models.Branch.objects, source="branch"
    )

    class Meta:
        model = deliveries_models.Delivery
        fields = serializers.ALL_FIELDS


class DeliveryProductSerializer(generic_base.DynamicFieldsModelSerializer):
    class Meta:
        model = deliveries_models.DeliveryProduct
        fields = serializers.ALL_FIELDS

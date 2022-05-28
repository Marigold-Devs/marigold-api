from backend.branches.serializers import base as branches_serializers_base
from rest_framework import serializers


class BranchCreateUpdateRequestSerializer(branches_serializers_base.BranchSerializer):
    class Meta:
        model = branches_serializers_base.BranchSerializer.Meta.model
        fields = "__all__"
        ref_name = "BranchCreateUpdateRequestSerializer"


class BranchProductConvertRequestSerializer(serializers.Serializer):
    from_branch_product_id = serializers.IntegerField(required=True)
    from_quantity = serializers.DecimalField(
        max_digits=10, decimal_places=3, required=True
    )
    to_branch_product_id = serializers.IntegerField(required=True)
    to_quantity = serializers.DecimalField(
        max_digits=10, decimal_places=3, required=True
    )

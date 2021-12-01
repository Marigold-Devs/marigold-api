from backend.branches import serializers as branches_serializers
from rest_framework import serializers


class BranchCreateUpdateRequestSerializer(branches_serializers.base.BranchSerializer):
    class Meta:
        model = branches_serializers.base.BranchSerializer.Meta.model
        fields = "__all__"
        ref_name = "BranchCreateUpdateRequestSerializer"

from rest_framework import serializers
from backend.branches import models as branches_models
from backend.generic.serializers import base as generic_base


class BranchProductsQuerySerializer(generic_base.DynamicFieldsModelSerializer):
    search = serializers.CharField(required=False)
    branch_id = serializers.IntegerField(required=True)

    class Meta:
        model = branches_models.Branch
        fields = ["branch_id", "search"]

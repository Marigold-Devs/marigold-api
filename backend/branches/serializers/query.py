from rest_framework import serializers
from backend.branches import models as branches_models
from backend.branches import choices as branches_choices
from backend.generic.serializers import base as generic_base


class BranchProductsQuerySerializer(generic_base.DynamicFieldsModelSerializer):
    branch_id = serializers.IntegerField(required=True)
    search = serializers.CharField(required=False)
    status = serializers.ChoiceField(
        required=False, choices=branches_choices.BRANCH_PRODUCT_STATUSES_CHOICES
    )

    class Meta:
        model = branches_models.Branch
        fields = ["branch_id", "search", "status"]

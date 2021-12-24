from backend.branches import models as branches_models
from backend.generic.serializers import base as generic_base
from backend.transactions import models as transactions_models
from rest_framework import serializers


class TransactionSerializer(generic_base.DynamicFieldsModelSerializer):
    branch_id = serializers.PrimaryKeyRelatedField(
        many=False, queryset=branches_models.Branch.objects, source="branch"
    )

    class Meta:
        model = transactions_models.Transaction
        fields = serializers.ALL_FIELDS


class TransactionProductSerializer(generic_base.DynamicFieldsModelSerializer):
    class Meta:
        model = transactions_models.TransactionProduct
        fields = serializers.ALL_FIELDS

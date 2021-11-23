from backend.generic.serializers import base as generic_base
from backend.preorders import models as preorders_models
from backend.branches import models as branches_models
from rest_framework import serializers


class PreordersSerializer(generic_base.DynamicFieldsModelSerializer):
    branch_id = serializers.PrimaryKeyRelatedField(
        many=False, queryset=branches_models.Branch.objects, source="branch"
    )

    class Meta:
        model = preorders_models.Preorder
        fields = serializers.ALL_FIELDS


class PreorderProductSerializer(generic_base.DynamicFieldsModelSerializer):
    class Meta:
        model = preorders_models.PreorderProduct
        fields = serializers.ALL_FIELDS


class PreorderTransactionSerializer(generic_base.DynamicFieldsModelSerializer):
    preorder_id = serializers.PrimaryKeyRelatedField(
        many=False, queryset=preorders_models.Preorder.objects, source="preorder"
    )

    class Meta:
        model = preorders_models.PreorderTransaction
        fields = serializers.ALL_FIELDS

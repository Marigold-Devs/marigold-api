from backend.branches import models as branches_models
from backend.generic.serializers import base as generic_base
from backend.transactions import models as transactions_models
from backend.transactions import serializers as transactions_serializers
from rest_framework import serializers


class TransactionCreateRequestSerializer(
    transactions_serializers.base.TransactionSerializer
):
    class TransactionProductCreateSerializer(generic_base.DynamicFieldsModelSerializer):
        branch_product_id = serializers.PrimaryKeyRelatedField(
            many=False,
            queryset=branches_models.BranchProduct.objects,
            source="branch_product",
        )

        class Meta:
            model = transactions_models.TransactionProduct
            ref_name = (
                "TransactionCreateRequestSerializer-TransactionProductCreateSerializer"
            )
            fields = [
                "branch_product_id",
                "price",
                "quantity",
            ]

    transaction_products = TransactionProductCreateSerializer(
        many=True,
    )

    class Meta:
        model = transactions_serializers.base.TransactionSerializer.Meta.model
        fields = [
            "branch_id",
            "amount_tendered",
            "transaction_products",
        ]
        ref_name = "TransactionCreateRequestSerializer"

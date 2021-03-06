from pkg_resources import require
from backend.branches import models as branches_models
from backend.generic.serializers import base as generic_base
from backend.preorders import choices as preorders_choices
from backend.preorders import models as preorders_models
from backend.preorders import serializers as preorders_serializers
from backend.users import models as users_models
from rest_framework import serializers


class PreorderCreateRequestSerializer(preorders_serializers.base.PreordersSerializer):
    class PreorderSupplierCreateSerializer(serializers.Serializer):
        id = serializers.PrimaryKeyRelatedField(
            many=False,
            queryset=users_models.Client.objects,
            required=False,
        )
        name = serializers.CharField(max_length=50)
        description = serializers.CharField(max_length=250)
        address = serializers.CharField(max_length=50)
        landline = serializers.CharField(
            max_length=50,
            required=False,
        )
        phone = serializers.CharField(
            max_length=50,
            required=False,
        )

    class PreorderProductCreateSerializer(generic_base.DynamicFieldsModelSerializer):
        branch_product_id = serializers.PrimaryKeyRelatedField(
            many=False,
            queryset=branches_models.BranchProduct.objects,
            source="branch_product",
        )

        class Meta:
            model = preorders_models.PreorderProduct
            ref_name = "PreorderCreateRequestSerializer-PreorderProductCreateSerializer"
            fields = ["branch_product_id", "quantity", "remarks"]

    supplier = PreorderSupplierCreateSerializer(required=False)

    preorder_products = PreorderProductCreateSerializer(
        many=True,
    )

    class Meta:
        model = preorders_serializers.base.PreordersSerializer.Meta.model
        fields = [
            "branch_id",
            "delivery_type",
            "description",
            "supplier",
            "preorder_products",
        ]
        ref_name = "PreorderCreateRequestSerializer"


class PreorderUpdateRequestSerializer(preorders_serializers.base.PreordersSerializer):
    class PreorderProductUpdateSerializer(generic_base.DynamicFieldsModelSerializer):
        branch_product_id = serializers.PrimaryKeyRelatedField(
            many=False,
            queryset=branches_models.BranchProduct.objects,
            source="branch_product",
        )

        class Meta:
            model = preorders_models.PreorderProduct
            ref_name = "PreorderUpdateRequestSerializer-PreorderProductCreateSerializer"
            fields = ["branch_product_id", "quantity", "remarks"]

    status = serializers.ChoiceField(
        choices=preorders_choices.PREORDER_STATUSES_CHOICES,
        required=False,
    )

    preorder_products = PreorderProductUpdateSerializer(many=True, required=False)

    class Meta:
        model = preorders_serializers.base.PreordersSerializer.Meta.model
        fields = ["description", "status", "preorder_products"]
        ref_name = "PreorderUpdateRequestSerializer"


class PreorderTransactionCreateRequestSerializer(
    preorders_serializers.base.PreorderTransactionSerializer
):
    preorder_id = serializers.IntegerField()

    class PreorderTransactionProductCreateSerializer(serializers.Serializer):
        preorder_product_id = serializers.IntegerField()

        quantity = serializers.IntegerField()

        class Meta:
            ref_name = "PreorderTransactionCreateRequestSerializer-PreorderTransactionProductCreateSerializer"
            fields = [
                "preorder_product_id",
                "quantity",
            ]

    preorder_transaction_products = PreorderTransactionProductCreateSerializer(
        many=True
    )

    class Meta:
        model = preorders_serializers.base.PreorderTransactionSerializer.Meta.model
        fields = ["preorder_id", "preorder_transaction_products"]
        ref_name = "PreorderTransactionCreateRequestSerializer"

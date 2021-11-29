from django.db.models.aggregates import Sum
from backend.preorders import serializers as preorders_serializers
from backend.preorders import models as preorders_models
from backend.branches import models as branches_models
from backend.products import models as products_models
from backend.users import serializers as users_serializers
from backend.branches import serializers as branches_serializers
from backend.branches import serializers as branches_serializers
from rest_framework import serializers
from backend.generic.serializers import base as generic_base


class PreorderResponseSerializer(preorders_serializers.base.PreordersSerializer):
    class PreorderProductResponseSerializer(generic_base.DynamicFieldsModelSerializer):
        branch_product = serializers.SerializerMethodField()

        fulfilled_quantity = serializers.SerializerMethodField()

        product_name = serializers.SerializerMethodField()

        unit_type_id = serializers.SerializerMethodField()

        def get_product_name(self, preorder_product):
            product = products_models.Product.objects.filter(
                product_prices__branch_products__preorder_products__id=preorder_product.id
            ).first()

            return product.name

        def get_unit_type_id(self, preorder_product):
            product_price = products_models.ProductPrice.objects.filter(
                branch_products__preorder_products__id=preorder_product.id
            ).first()

            return product_price.unit_type_id

        def get_branch_product(self, preorder_product):
            branch_product = branches_models.BranchProduct.objects.filter(
                pk=preorder_product.branch_product_id
            ).first()

            return branches_serializers.base.BranchProductProductSerializer(
                branch_product
            ).data

        def get_fulfilled_quantity(self, preorder_product):
            return preorders_models.PreorderTransactionProduct.objects.filter(
                preorder_product=preorder_product
            ).aggregate(Sum("quantity"))["quantity__sum"]

        class Meta:
            model = preorders_models.PreorderProduct
            ref_name = "PreorderResponseSerializer-PreorderProductResponseSerializer"
            fields = serializers.ALL_FIELDS

    class PreorderTransactionsResponseSerializer(
        generic_base.DynamicFieldsModelSerializer
    ):
        preorder_transaction_products = (
            preorders_serializers.base.PreorderTransactionProductsSerializer(many=True)
        )

        user = users_serializers.base.UserSerializer()

        class Meta:
            model = preorders_models.PreorderTransaction
            ref_name = (
                "PreorderResponseSerializer-PreorderTransactionsResponseSerializer"
            )
            fields = serializers.ALL_FIELDS

    preorder_products = PreorderProductResponseSerializer(many=True)

    branch = branches_serializers.base.BranchesSerializer()

    user = users_serializers.base.UserSerializer()

    supplier = users_serializers.base.ClientSerializer()

    preorder_transactions = PreorderTransactionsResponseSerializer(many=True)

    class Meta:
        model = preorders_serializers.base.PreordersSerializer.Meta.model
        fields = serializers.ALL_FIELDS
        ref_name = "PreorderResponseSerializer"

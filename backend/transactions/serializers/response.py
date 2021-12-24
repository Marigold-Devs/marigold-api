from backend.branches import serializers as branches_serializers
from backend.generic.serializers import base as generic_base
from backend.products import serializers as products_serializers
from backend.transactions import models as transactions_models
from backend.transactions import serializers as transactions_serializers
from backend.users import serializers as users_serializers
from rest_framework import serializers


class TransactionResponseSerializer(transactions_serializers.base.TransactionSerializer):
    class TransactionProductResponseSerializer(generic_base.DynamicFieldsModelSerializer):
        product = serializers.SerializerMethodField()

        product_price = serializers.SerializerMethodField()

        branch_product = serializers.SerializerMethodField()

        unit_type = serializers.SerializerMethodField()

        def get_product(self, transaction_product):
            product = transaction_product.branch_product.product_price.product
            return products_serializers.base.ProductSerializer(product).data

        def get_product_price(self, transaction_product):
            product_price = transaction_product.branch_product.product_price
            return products_serializers.base.ProductPriceSerializer(product_price).data

        def get_branch_product(self, transaction_product):
            branch_product = transaction_product.branch_product
            return branches_serializers.base.BranchProductSerializer(
                branch_product
            ).data

        def get_unit_type(self, transaction_product):
            unit_type = transaction_product.branch_product.product_price.unit_type
            return products_serializers.base.UnitTypeSerializer(unit_type).data

        class Meta:
            model = transactions_models.TransactionProduct
            ref_name = "TransactionResponseSerializer-TransactionProductResponseSerializer"
            fields = serializers.ALL_FIELDS

    transaction_products = TransactionProductResponseSerializer(many=True)

    branch = branches_serializers.base.BranchSerializer()

    cashier = users_serializers.base.UserSerializer()

    class Meta:
        model = transactions_serializers.base.TransactionSerializer.Meta.model
        fields = serializers.ALL_FIELDS
        ref_name = "TransactionResponseSerializer"

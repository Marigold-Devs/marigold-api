from backend.branches import serializers as branches_serializers
from backend.branches import models as branches_models
from backend.branches.globals import BRANCH_PRODUCT_STATUSES
from backend.generic.serializers import base as generic_base
from backend.products import models as products_models
from backend.products import serializers as products_serializers
from rest_framework import serializers
from rest_framework import serializers
from drf_yasg.utils import swagger_serializer_method


class BranchProductsResponseSerializer(products_serializers.base.ProductSerializer):
    class ProductPriceSerializer(products_serializers.base.ProductPriceSerializer):
        balance = serializers.SerializerMethodField()

        def get_balance(self, product_price):
            branch_id = self.context.get("branch_id")

            branch_product = branches_models.BranchProduct.objects.filter(
                branch_id=branch_id, product_price_id=product_price.id
            ).first()

            return branch_product.balance if branch_product is not None else None

        class Meta:
            ref_name = "BranchProductsResponseSerializer-ProductPriceSerializer"
            model = products_serializers.base.ProductPriceSerializer.Meta.model
            fields = products_serializers.base.ProductPriceSerializer.Meta.fields + [
                "balance",
            ]

    def get_status(self, product):
        branch_id = self.context.get("branch_id")

        # Get product prices
        product_prices = products_models.ProductPrice.objects.filter(
            product_id=product.id
        )

        # Get branch products
        branch_products = []
        for product_price in product_prices:

            branch_product = branches_models.BranchProduct.objects.filter(
                branch_id=branch_id, product_price_id=product_price.id
            ).first()
            branch_products.append(branch_product)

            # Check if status is REORDER
            if (
                product_price.reorder_point > 0
                and branch_product.balance > 0
                and branch_product.balance <= product_price.reorder_point
            ):
                return BRANCH_PRODUCT_STATUSES["REORDER"]

        # Check if balance is all zero
        total = 0
        for branch_product in branch_products:
            total += branch_product.balance

        if total == 0:
            return BRANCH_PRODUCT_STATUSES["OUT_OF_STOCK"]

        return BRANCH_PRODUCT_STATUSES["AVAILABLE"]

    product_prices = ProductPriceSerializer(many=True)
    status = serializers.SerializerMethodField()

    class Meta:
        model = products_serializers.base.ProductSerializer.Meta.model
        fields = ["name", "unit_cost", "vat_type", "product_prices", "status"]
        ref_name = "BranchProductsResponseSerializer"

from backend.products import serializers as products_serializers
from backend.users import serializers as users_serializers
from rest_framework import serializers
from backend.products import models as products_models


class TopProductsResponseSerializer(products_serializers.base.ProductSerializer):
    class ProductPriceSerializer(products_serializers.base.ProductPriceSerializer):
        total_sales = serializers.SerializerMethodField()

        total_quantity = serializers.SerializerMethodField()

        unit_type = serializers.SerializerMethodField()

        def get_total_sales(self, product_price):
            branch_id = self.context.get("branch_id")
            date_range = self.context.get("date_range")

            product_price = (
                products_models.ProductPrice.objects.filter(pk=product_price.id)
                .with_sales(branch_id=branch_id, date_range=date_range)
                .first()
            )

            return product_price.total_sales

        def get_total_quantity(self, product_price):
            branch_id = self.context.get("branch_id")
            date_range = self.context.get("date_range")

            product_price = (
                products_models.ProductPrice.objects.filter(pk=product_price.id)
                .with_quantity(branch_id=branch_id, date_range=date_range)
                .first()
            )

            return product_price.total_quantity

        def get_unit_type(self, product_price):
            unit_type = product_price.unit_type
            return products_serializers.base.UnitTypeSerializer(unit_type).data

        class Meta:
            ref_name = "TopProductsResponseSerializer-ProductPriceSerializer"
            model = products_serializers.base.ProductPriceSerializer.Meta.model
            fields = products_serializers.base.ProductPriceSerializer.Meta.fields + [
                "total_sales",
                "total_quantity",
                "unit_type",
            ]

    product_prices = ProductPriceSerializer(many=True)

    total_sales = serializers.DecimalField(default=0, max_digits=10, decimal_places=3)

    class Meta:
        model = products_serializers.base.ProductSerializer.Meta.model
        fields = ["id", "name", "total_sales", "product_prices"]
        ref_name = "TopProductsResponseSerializer"


class TopCustomersResponseSerializer(users_serializers.base.ClientSerializer):
    total_purchase = serializers.DecimalField(
        default=0, max_digits=10, decimal_places=3
    )

    class Meta:
        model = users_serializers.base.ClientSerializer.Meta.model
        fields = ["id", "name", "total_purchase"]
        ref_name = "TopCustomersResponseSerializer"

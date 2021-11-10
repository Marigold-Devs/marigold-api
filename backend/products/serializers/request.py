from backend.products import serializers as products_serializers
from backend.products import models as products_models
from backend.generic.serializers import base as generic_base
from rest_framework import serializers


class ProductCreateRequestSerializer(products_serializers.base.ProductSerializer):
    class ProductPriceCreateSerializer(generic_base.DynamicFieldsModelSerializer):
        unit_type_id = serializers.IntegerField()

        class Meta:
            model = products_models.ProductPrice
            ref_name = "ProductCreateRequestSerializer-ProductPriceCreateSerializer"
            fields = [
                "unit_type_id",
                "price_market",
                "price_delivery",
                "price_pickup",
                "price_special",
                "reorder_point",
            ]

    product_prices = ProductPriceCreateSerializer(
        many=True,
    )

    class Meta:
        model = products_serializers.base.ProductSerializer.Meta.model
        fields = "__all__"
        ref_name = "ProductCreateRequestSerializer"


class ProductUpdateRequestSerializer(products_serializers.base.ProductSerializer):
    class ProductPriceUpdateSerializer(generic_base.DynamicFieldsModelSerializer):
        id = serializers.IntegerField(required=False)
        unit_type_id = serializers.IntegerField(required=True)

        class Meta:
            model = products_models.ProductPrice
            ref_name = "ProductUpdateRequestSerializer-ProductPriceUpdateSerializer"
            fields = (
                "id",
                "unit_type_id",
                "price_market",
                "price_delivery",
                "price_pickup",
                "price_special",
                "reorder_point",
            )

    product_prices = ProductPriceUpdateSerializer(
        many=True,
    )

    class Meta:
        model = products_serializers.base.ProductSerializer.Meta.model
        fields = "__all__"
        ref_name = "ProductUpdateRequestSerializer"

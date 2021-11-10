from backend.products import serializers as products_serializers
from rest_framework import serializers


class ProductResponseSerializer(products_serializers.base.ProductSerializer):
    product_prices = products_serializers.base.ProductPriceSerializer(
        many=True,
    )

    class Meta:
        model = products_serializers.base.ProductSerializer.Meta.model
        fields = "__all__"
        ref_name = "ProductCreateResponseSerializer"

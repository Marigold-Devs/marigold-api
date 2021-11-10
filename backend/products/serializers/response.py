from backend.products import serializers as product_serializers
from rest_framework import serializers


class ProductResponseSerializer(product_serializers.base.ProductSerializer):
    product_prices = product_serializers.base.ProductPriceSerializer(
        many=True,
    )

    class Meta:
        model = product_serializers.base.ProductSerializer.Meta.model
        fields = "__all__"
        ref_name = "ProductCreateResponseSerializer"

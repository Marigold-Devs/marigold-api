from backend.products import serializers as products_serializers
from backend.users import serializers as users_serializers
from rest_framework import serializers


class TopProductsResponseSerializer(products_serializers.base.ProductSerializer):
    total_purchase = serializers.DecimalField(
        default=0, max_digits=10, decimal_places=3
    )

    class Meta:
        model = products_serializers.base.ProductSerializer.Meta.model
        fields = ["id", "name", "total_purchase"]
        ref_name = "TopProductsResponseSerializer"


class TopCustomersResponseSerializer(users_serializers.base.ClientSerializer):
    total_purchase = serializers.DecimalField(
        default=0, max_digits=10, decimal_places=3
    )

    class Meta:
        model = users_serializers.base.ClientSerializer.Meta.model
        fields = ["id", "name", "total_purchase"]
        ref_name = "TopCustomersResponseSerializer"

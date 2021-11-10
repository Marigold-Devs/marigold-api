from backend.generic.serializers import base as generic_base
from backend.products import models as products_models


class ProductSerializer(generic_base.DynamicFieldsModelSerializer):
    class Meta:
        model = products_models.Product
        fields = "__all__"


class ProductPriceSerializer(generic_base.DynamicFieldsModelSerializer):
    class Meta:
        model = products_models.ProductPrice
        fields = [
            "id",
            "product_id",
            "unit_type_id",
            "price_market",
            "price_delivery",
            "price_pickup",
            "price_special",
            "reorder_point",
        ]

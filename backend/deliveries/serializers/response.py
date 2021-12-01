from backend.branches import models as branches_models
from backend.branches import serializers as branches_serializers
from backend.deliveries import models as deliveries_models
from backend.deliveries import serializers as deliveries_serializers
from backend.generic.serializers import base as generic_base
from backend.products import serializers as products_serializers
from backend.branches import serializers as branches_serializers
from backend.users import serializers as users_serializers
from rest_framework import serializers


class DeliveryResponseSerializer(deliveries_serializers.base.DeliverySerializer):
    class DeliveryProductResponseSerializer(generic_base.DynamicFieldsModelSerializer):
        product = serializers.SerializerMethodField()

        product_price = serializers.SerializerMethodField()

        branch_product = serializers.SerializerMethodField()

        unit_type = serializers.SerializerMethodField()

        def get_product(self, delivery_product):
            product = delivery_product.branch_product.product_price.product
            return products_serializers.base.ProductSerializer(product).data

        def get_product_price(self, delivery_product):
            product_price = delivery_product.branch_product.product_price
            return products_serializers.base.ProductPriceSerializer(product_price).data

        def get_branch_product(self, delivery_product):
            branch_product = delivery_product.branch_product
            return branches_serializers.base.BranchProductSerializer(
                branch_product
            ).data

        def get_unit_type(self, delivery_product):
            unit_type = delivery_product.branch_product.product_price.unit_type
            return products_serializers.base.UnitTypeSerializer(unit_type).data

        class Meta:
            model = deliveries_models.DeliveryProduct
            ref_name = "DeliveryResponseSerializer-DeliveryProductResponseSerializer"
            fields = serializers.ALL_FIELDS

    delivery_products = DeliveryProductResponseSerializer(many=True)

    branch = branches_serializers.base.BranchSerializer()

    user = users_serializers.base.UserSerializer()

    customer = users_serializers.base.ClientSerializer()

    class Meta:
        model = deliveries_serializers.base.DeliverySerializer.Meta.model
        fields = serializers.ALL_FIELDS
        ref_name = "DeliveryResponseSerializer"

from backend.deliveries import serializers as deliveries_serializers
from backend.deliveries import models as deliveries_models
from backend.branches import models as branches_models
from backend.users import serializers as users_serializers
from backend.branches import serializers as branches_serializers
from rest_framework import serializers
from backend.generic.serializers import base as generic_base


class DeliveryResponseSerializer(deliveries_serializers.base.DeliverySerializer):
    class DeliveryProductResponseSerializer(generic_base.DynamicFieldsModelSerializer):
        branch_product = serializers.SerializerMethodField()

        def get_branch_product(self, delivery_product):
            branch_product = branches_models.BranchProduct.objects.filter(
                pk=delivery_product.branch_product_id
            ).first()

            return branches_serializers.base.BranchProductProductSerializer(
                branch_product
            ).data

        class Meta:
            model = deliveries_models.DeliveryProduct
            ref_name = "DeliveryResponseSerializer-DeliveryProductResponseSerializer"
            fields = serializers.ALL_FIELDS

    delivery_products = DeliveryProductResponseSerializer(many=True)

    branch = branches_serializers.base.BranchesSerializer()

    user = users_serializers.base.UserSerializer()

    customer = users_serializers.base.ClientSerializer()

    class Meta:
        model = deliveries_serializers.base.DeliverySerializer.Meta.model
        fields = serializers.ALL_FIELDS
        ref_name = "DeliveryResponseSerializer"

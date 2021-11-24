from backend.generic.serializers import base as generic_base
from backend.deliveries import models as deliveries_models
from backend.branches import models as branches_models
from backend.users import models as users_models
from backend.deliveries import serializers as deliveries_serializers
from rest_framework import serializers


class DeliveryCreateRequestSerializer(deliveries_serializers.base.DeliverySerializer):
    class DeliveryCustomerCreateSerializer(serializers.Serializer):
        id = serializers.PrimaryKeyRelatedField(
            many=False,
            queryset=users_models.Client.objects,
            required=False,
        )
        name = serializers.CharField(max_length=50)
        description = serializers.CharField(max_length=250)
        address = serializers.CharField(max_length=50)
        landline = serializers.CharField(
            max_length=50,
            required=False,
        )
        phone = serializers.CharField(
            max_length=50,
            required=False,
        )

    class DeliveryProductCreateSerializer(generic_base.DynamicFieldsModelSerializer):
        branch_product_id = serializers.PrimaryKeyRelatedField(
            many=False,
            queryset=branches_models.BranchProduct.objects,
            source="branch_product",
        )

        class Meta:
            model = deliveries_models.DeliveryProduct
            ref_name = "DeliveryCreateRequestSerializer-DeliveryProductCreateSerializer"
            fields = [
                "branch_product_id",
                "quantity",
            ]

    customer = DeliveryCustomerCreateSerializer(required=False)

    delivery_products = DeliveryProductCreateSerializer(
        many=True,
    )

    class Meta:
        model = deliveries_serializers.base.DeliverySerializer.Meta.model
        fields = [
            "branch_id",
            "delivery_type",
            "customer",
            "delivery_products",
            "datetime_delivery",
        ]
        ref_name = "DeliveryCreateRequestSerializer"


class DeliveryUpdateRequestSerializer(deliveries_serializers.base.DeliverySerializer):
    class Meta:
        model = deliveries_serializers.base.DeliverySerializer.Meta.model
        fields = [
            "status",
            "prepared_by",
            "checked_by",
            "pulled_out_by",
            "delivered_by",
        ]
        ref_name = "DeliveryUpdateRequestSerializer"

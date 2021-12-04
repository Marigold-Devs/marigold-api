from backend.notifications import serializers as notifications_serializers
from rest_framework import serializers
from backend.products import serializers as products_serializers
from backend.branches import globals as branches_globals


class NotificationResponseSerializer(
    notifications_serializers.base.NotificationSerializer
):
    product = serializers.SerializerMethodField()

    unit_type = serializers.SerializerMethodField()

    status = serializers.SerializerMethodField()

    def get_product(self, notification):
        product = notification.branch_product.product_price.product
        return products_serializers.base.ProductSerializer(product).data

    def get_unit_type(self, notification):
        unit_type = notification.branch_product.product_price.unit_type
        return products_serializers.base.UnitTypeSerializer(unit_type).data

    def get_status(self, notification):
        return notification.branch_product.get_status()

    class Meta:
        model = notifications_serializers.base.NotificationSerializer.Meta.model
        fields = serializers.ALL_FIELDS
        ref_name = "NotificationResponseSerializer"

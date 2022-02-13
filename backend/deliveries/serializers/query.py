from backend.deliveries import choices as deliveries_choices
from rest_framework import serializers


class DeliveryQuerySerializer(serializers.Serializer):
    payment_status = serializers.ChoiceField(
        required=False, choices=deliveries_choices.PAYMENT_STATUSES_CHOICES
    )

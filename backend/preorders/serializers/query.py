from backend.preorders import choices as preorders_choices
from rest_framework import serializers


class PreordersQuerySerializer(serializers.Serializer):
    date_created = serializers.DateField(required=False)

    date_fulfilled = serializers.DateField(required=False)
    
    status = serializers.ChoiceField(
        required=False, choices=preorders_choices.PREORDER_STATUSES_CHOICES
    )

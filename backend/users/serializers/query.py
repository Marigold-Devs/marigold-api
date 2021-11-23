from backend.users import choices as users_choices
from rest_framework import serializers


class ClientQuerySerializer(serializers.Serializer):
    type = serializers.ChoiceField(
        required=False, choices=users_choices.CLIENT_TYPE_CHOICES
    )

from backend.users import choices as users_choices
from rest_framework import serializers


class UserQuerySerializer(serializers.Serializer):
    user_type = serializers.ChoiceField(
        required=False, choices=users_choices.USER_TYPE_CHOICES
    )

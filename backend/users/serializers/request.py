from backend.users import choices as users_choices
from backend.users import models as users_models
from django.db.models import Q
from rest_framework import serializers


class LoginRequestSerializer(serializers.Serializer):
    """Login Request Serializer

    Serializer for login requests. Verifies login credentials.
    """

    login = serializers.CharField()
    password = serializers.CharField(style={"input_type": "password"})

    def validate(self, attrs):
        """Validate login credentials.

        Checks that either email or username exists
        """
        try:
            attrs["user"] = users_models.User.objects.get(Q(username=attrs["login"]))
        except users_models.User.DoesNotExist:
            attrs["user"] = None

        return attrs

    class Meta:
        ref_name = "LoginRequestSerializerV4"


class UserCreateRequestSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    email = serializers.CharField()
    username = serializers.CharField(max_length=20)
    user_type = serializers.ChoiceField(choices=users_choices.USER_TYPE_CHOICES)
    first_name = serializers.CharField(max_length=30)
    last_name = serializers.CharField(max_length=30)
    display_name = serializers.CharField(
        max_length=30, required=False, allow_null=True, allow_blank=True
    )
    contact_number = serializers.CharField(
        max_length=15, required=False, allow_null=True, allow_blank=True
    )
    password = serializers.CharField(max_length=100, allow_blank=True)

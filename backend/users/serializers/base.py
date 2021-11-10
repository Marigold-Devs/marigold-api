from backend.generic.serializers import base as generic_base
from backend.users import models as users_models


class UserSerializer(generic_base.DynamicFieldsModelSerializer):
    class Meta:
        model = users_models.User
        fields = (
            "id",
            "username",
            "user_type",
            "first_name",
            "last_name",
        )

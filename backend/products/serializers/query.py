from backend.preorders import choices as preorders_choices
from rest_framework import serializers
from backend.generic import serializers as generic_serializers


class ProductsQuerySerializer(serializers.Serializer):
    ids = generic_serializers.fields.CommaSeparatedIntegersField(required=False)

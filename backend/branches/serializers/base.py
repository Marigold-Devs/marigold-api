from rest_framework.serializers import ALL_FIELDS
from backend.branches import models as branches_models
from backend.products import models as products_models
from backend.products import serializers as products_serializers
from backend.generic.serializers import base as generic_base


class BranchesSerializer(generic_base.DynamicFieldsModelSerializer):
    class Meta:
        model = branches_models.Branch
        fields = ALL_FIELDS


class BranchProductsSerializer(generic_base.DynamicFieldsModelSerializer):
    class Meta:
        model = branches_models.BranchProduct
        fields = ALL_FIELDS


class BranchProductProductSerializer(generic_base.DynamicFieldsModelSerializer):
    class ProductPriceProductSerializer(generic_base.DynamicFieldsModelSerializer):
        product = products_serializers.base.ProductSerializer()

        class Meta:
            model = products_serializers.base.ProductPriceSerializer.Meta.model
            ref_name = "BranchProductProductSerializer-ProductPriceProductSerializer"
            fields = ALL_FIELDS

    product_price = ProductPriceProductSerializer()

    class Meta:
        model = branches_models.BranchProduct
        fields = "__all__"

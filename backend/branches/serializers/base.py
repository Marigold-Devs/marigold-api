from backend.branches import models as branches_models
from backend.generic.serializers import base as generic_base


class BranchesSerializer(generic_base.DynamicFieldsModelSerializer):
    class Meta:
        model = branches_models.Branch
        fields = "__all__"


class BranchProductsSerializer(generic_base.DynamicFieldsModelSerializer):
    class Meta:
        model = branches_models.BranchProduct
        fields = "__all__"

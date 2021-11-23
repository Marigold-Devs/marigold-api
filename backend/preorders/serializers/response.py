from backend.preorders import serializers as preorders_serializers
from backend.preorders import models as preorders_models
from backend.branches import models as branches_models
from backend.users import serializers as users_serializers
from backend.branches import serializers as branches_serializers
from backend.branches import serializers as branches_serializers
from rest_framework import serializers
from backend.generic.serializers import base as generic_base


class PreorderResponseSerializer(preorders_serializers.base.PreordersSerializer):
    class PreorderProductResponseSerializer(generic_base.DynamicFieldsModelSerializer):
        branch_product = serializers.SerializerMethodField()

        def get_branch_product(self, preorder_product):
            branch_product = branches_models.BranchProduct.objects.filter(
                pk=preorder_product.branch_product_id
            ).first()

            return branches_serializers.base.BranchProductProductSerializer(
                branch_product
            ).data

        class Meta:
            model = preorders_models.PreorderProduct
            ref_name = "PreorderResponseSerializer-PreorderProductResponseSerializer"
            fields = serializers.ALL_FIELDS

    preorder_products = PreorderProductResponseSerializer(many=True)

    branch = branches_serializers.base.BranchesSerializer()

    user = users_serializers.base.UserSerializer()

    supplier = users_serializers.base.ClientSerializer()

    class Meta:
        model = preorders_serializers.base.PreordersSerializer.Meta.model
        fields = serializers.ALL_FIELDS
        ref_name = "PreorderResponseSerializer"

from backend.generic.serializers import base as generic_base
from backend.preorders import models as preorders_models
from backend.branches import models as branches_models
from backend.products import models as products_models
from rest_framework import serializers


class PreordersSerializer(generic_base.DynamicFieldsModelSerializer):
    branch_id = serializers.PrimaryKeyRelatedField(
        many=False, queryset=branches_models.Branch.objects, source="branch"
    )

    class Meta:
        model = preorders_models.Preorder
        fields = serializers.ALL_FIELDS


class PreorderProductSerializer(generic_base.DynamicFieldsModelSerializer):
    class Meta:
        model = preorders_models.PreorderProduct
        fields = serializers.ALL_FIELDS


class PreorderTransactionSerializer(generic_base.DynamicFieldsModelSerializer):
    preorder_id = serializers.PrimaryKeyRelatedField(
        many=False, queryset=preorders_models.Preorder.objects, source="preorder"
    )

    class Meta:
        model = preorders_models.PreorderTransaction
        fields = serializers.ALL_FIELDS


class PreorderTransactionProductsSerializer(generic_base.DynamicFieldsModelSerializer):
    product_name = serializers.SerializerMethodField()
    unit_type_id = serializers.SerializerMethodField()

    def get_product_name(self, preorder_transaction_product):
        product = products_models.Product.objects.filter(
            product_prices__branch_products__preorder_products__id=preorder_transaction_product.preorder_product_id
        ).first()

        return product.name

    def get_unit_type_id(self, preorder_transaction_product):
        product_price = products_models.ProductPrice.objects.filter(
            branch_products__preorder_products__id=preorder_transaction_product.preorder_product_id
        ).first()

        return product_price.unit_type_id

    class Meta:
        model = preorders_models.PreorderTransactionProduct
        fields = serializers.ALL_FIELDS

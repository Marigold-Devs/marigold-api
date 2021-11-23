from backend.generic.swagger import STRING_RESPONSE
from backend.generic.views import BaseViewSet
from backend.preorders import globals as preorders_globals
from backend.preorders import models as preorders_models
from backend.preorders import serializers as preorders_serializers
from backend.users import models as users_models
from backend.users.globals import CLIENT_TYPES
from django.db import transaction
from drf_yasg.utils import swagger_auto_schema
from rest_framework import mixins, status
from rest_framework.response import Response


class PreorderViewSet(
    BaseViewSet,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
):
    queryset = preorders_models.Preorder.objects.all()
    serializer_class = preorders_serializers.response.PreorderResponseSerializer

    def list(self, request, *args, **kwargs):
        """List Preorders

        Gets a collection of Preorders.
        """
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        """Retrieve Preorder

        Gets a Preorder.
        """
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        request_body=preorders_serializers.request.PreorderCreateRequestSerializer(),
        responses={201: preorders_serializers.response.PreorderResponseSerializer()},
    )
    @transaction.atomic
    def create(self, request, *args, **kwargs):
        """Create a Preorder

        Create a new Preorder.
        """

        serializer = preorders_serializers.request.PreorderCreateRequestSerializer(
            data=request.data
        )
        serializer.is_valid(raise_exception=True)

        # Create or update client
        supplier = serializer.validated_data["supplier"]
        supplier_obj = supplier.get("id", None)
        supplier_id = supplier_obj.id if supplier_obj is not None else None
        client, created = users_models.Client.objects.update_or_create(
            pk=supplier_id,
            defaults={
                "name": supplier["name"],
                "description": supplier["description"],
                "address": supplier["address"],
                "landline": supplier.get("landline", None),
                "phone": supplier.get("phone", None),
                "type": CLIENT_TYPES["SUPPLIER"],
            },
        )

        # Create preorder
        preorder = preorders_models.Preorder.objects.create(
            branch=serializer.validated_data["branch"],
            user=request.user,
            supplier=client,
            delivery_type=serializer.validated_data["delivery_type"],
            status=preorders_globals.PREORDER_STATUSES["PENDING"],
        )

        # Create preorder products
        preorder_products_data = []
        for preorder_product in serializer.validated_data["preorder_products"]:
            preorder_products_data.append(
                preorders_models.PreorderProduct(
                    preorder=preorder,
                    branch_product=preorder_product["branch_product"],
                    quantity=preorder_product["quantity"],
                )
            )
        preorders_models.PreorderProduct.objects.bulk_create(preorder_products_data)

        # Create response
        response = preorders_serializers.response.PreorderResponseSerializer(preorder)

        return Response(response.data)

    @swagger_auto_schema(
        request_body=preorders_serializers.request.PreorderUpdateRequestSerializer(),
        responses={200: preorders_serializers.response.PreorderResponseSerializer()},
    )
    def partial_update(self, request, *args, **kwargs):
        """Update Preorder Partially

        Partially updates a preorder.
        """
        serializer = preorders_serializers.request.PreorderUpdateRequestSerializer(
            data=request.data
        )
        serializer.is_valid(raise_exception=True)

        # Update preorder
        preorder = self.get_object()
        setattr(preorder, "status", serializer.validated_data["status"])
        preorder.save()

        # Create response
        response = preorders_serializers.response.PreorderResponseSerializer(preorder)

        return Response(response.data)


class PreorderTransactionViewSet(
    BaseViewSet,
    mixins.CreateModelMixin,
):
    queryset = preorders_models.PreorderTransaction.objects.all()

    @swagger_auto_schema(
        request_body=preorders_serializers.request.PreorderTransactionCreateRequestSerializer(),
        responses={204: "No Content", 401: STRING_RESPONSE},
    )
    def create(self, request, *args, **kwargs):
        """Create a Preorder Transaction

        Create a new Preorder Transaction.
        """

        serializer = (
            preorders_serializers.request.PreorderTransactionCreateRequestSerializer(
                data=request.data
            )
        )
        serializer.is_valid(raise_exception=True)

        # Check if preorder is not yet submitted
        preorder = preorders_models.Preorder.objects.filter(
            pk=serializer.validated_data["preorder_id"]
        )
        if preorder["status"] != preorders_globals.PREORDER_STATUSES["APPROVED"]:
            return Response(
                "Preorder status is not 'Approved'", status=status.HTTP_400_BAD_REQUEST
            )

        # Create preorder transaction
        preorder_transaction = preorders_models.PreorderTransaction.objects.create(
            preorder_id=serializer.validated_data["preorder_id"],
            user=request.user,
        )

        # Create preorder transaction products
        preorder_transaction_products_data = []
        for preorder_transaction_product in serializer.validated_data[
            "preorder_transaction_products"
        ]:
            preorder_transaction_products_data.append(
                preorders_models.PreorderProduct(
                    preorder_transaction=preorder_transaction,
                    preorder_product_id=preorder_transaction_product[
                        "preorder_product_id"
                    ],
                    quantity=preorder_transaction_product["quantity"],
                )
            )
        preorders_models.PreorderTransactionProduct.objects.bulk_create(
            preorder_transaction_products_data
        )

        return Response(status=status.HTTP_204_NO_CONTENT)

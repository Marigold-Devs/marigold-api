from backend.branches import models as branches_models
from backend.generic.swagger import STRING_RESPONSE
from backend.generic.views import BaseViewSet
from backend.preorders import globals as preorders_globals
from backend.preorders import models as preorders_models
from backend.preorders import serializers as preorders_serializers
from backend.users import models as users_models
from backend.users.globals import CLIENT_TYPES
from django.db import transaction
from django.utils import timezone
from drf_yasg.utils import swagger_auto_schema
from rest_framework import filters, mixins, status
from rest_framework.response import Response


class PreorderViewSet(
    BaseViewSet,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
):
    queryset = preorders_models.Preorder.objects.all().order_by("-id")
    serializer_class = preorders_serializers.response.PreorderResponseSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    ordering_fields = ["id"]
    ordering = ["-id"]
    search_fields = [
        "id",
        "supplier__name",
    ]

    def get_queryset(self):
        queryset = super().get_queryset()
        request = self.request

        serializer = preorders_serializers.query.PreordersQuerySerializer(
            data=request.query_params
        )
        serializer.is_valid(raise_exception=True)

        date_created = serializer.validated_data.get("date_created", None)
        if date_created is not None:
            print(date_created)
            queryset = queryset.with_date_created(date_created)

        date_fulfilled = serializer.validated_data.get("date_fulfilled", None)
        if date_fulfilled is not None:
            queryset = queryset.with_date_fulfilled(date_fulfilled)

        status = serializer.validated_data.get("status", None)
        if status is not None:
            queryset = queryset.with_status(status)

        return queryset.all()

    @swagger_auto_schema(
        query_serializer=preorders_serializers.query.PreordersQuerySerializer,
        responses={200: preorders_serializers.response.PreorderResponseSerializer},
    )
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
            description=serializer.validated_data.get("description", None),
        )

        # Create preorder products
        preorder_products_data = []
        for preorder_product in serializer.validated_data["preorder_products"]:
            preorder_products_data.append(
                preorders_models.PreorderProduct(
                    preorder=preorder,
                    branch_product=preorder_product["branch_product"],
                    quantity=preorder_product["quantity"],
                    remarks=preorder_product.get("remarks", None),
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
    @transaction.atomic
    def partial_update(self, request, *args, **kwargs):
        """Update Preorder Partially

        Partially updates a preorder.
        """
        serializer = preorders_serializers.request.PreorderUpdateRequestSerializer(
            data=request.data
        )
        serializer.is_valid(raise_exception=True)

        preorder = self.get_object()

        status = serializer.validated_data.get("status")
        if status:
            setattr(preorder, "status", status)

            if status == preorders_globals.PREORDER_STATUSES["DELIVERED"]:
                setattr(preorder, "datetime_fulfilled", timezone.now())

                # Get preorder transaction products
                quantity_sum = {}

                for preorder_transaction in preorder.preorder_transactions.all():
                    preorder_transaction_products = (
                        preorder_transaction.preorder_transaction_products.all()
                    )

                    for preorder_transaction_product in preorder_transaction_products:
                        branch_product_id = (
                            preorder_transaction_product.preorder_product.branch_product_id
                        )

                        quantity = int(preorder_transaction_product.quantity)
                        quantity_sum[branch_product_id] = (
                            quantity_sum.get(branch_product_id, 0) + quantity
                        )

                # Add new quantity into branch product's balance
                for branch_product_id, quantity in quantity_sum.items():
                    branch_product = branches_models.BranchProduct.objects.get(
                        pk=branch_product_id
                    )
                    branch_product.balance += quantity
                    branch_product.save()

                    # Check for possible notifications
                    branch_product.update_notification()

        description = serializer.validated_data.get("description")
        if description:
            setattr(preorder, "description", description)

        preorder_products = serializer.validated_data.get("preorder_products")
        if preorder_products:
            # Delete all preorder products first
            preorder.preorder_products.all().delete()

            # Recreate preorder products
            preorder_products_data = []
            for preorder_product in serializer.validated_data["preorder_products"]:
                preorder_products_data.append(
                    preorders_models.PreorderProduct(
                        preorder=preorder,
                        branch_product=preorder_product["branch_product"],
                        quantity=preorder_product["quantity"],
                        remarks=preorder_product.get("remarks", None),
                    )
                )
            preorders_models.PreorderProduct.objects.bulk_create(preorder_products_data)

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
    @transaction.atomic
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
        ).first()
        if preorder.status != preorders_globals.PREORDER_STATUSES["APPROVED"]:
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
                preorders_models.PreorderTransactionProduct(
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

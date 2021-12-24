from backend.branches import models as branches_models
from backend.generic.views import BaseViewSet
from backend.transactions import models as transactions_models
from backend.transactions import serializers as transactions_serializers
from backend.users import models as users_models
from backend.users.globals import CLIENT_TYPES
from django.db import transaction
from drf_yasg.utils import swagger_auto_schema
from rest_framework import mixins
from rest_framework.response import Response


class TransactionViewSet(
    BaseViewSet,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
):
    queryset = transactions_models.Transaction.objects.all().order_by("-id")
    serializer_class = transactions_serializers.response.TransactionResponseSerializer

    def list(self, request, *args, **kwargs):
        """List Transactions

        Gets a collection of Transaction.
        """
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        """Retrieve Transaction

        Gets a Transaction.
        """
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        request_body=transactions_serializers.request.TransactionCreateRequestSerializer(),
        responses={
            201: transactions_serializers.response.TransactionResponseSerializer
        },
    )
    @transaction.atomic
    def create(self, request, *args, **kwargs):
        """Create a Transaction

        Create a new Transaction.
        """

        serializer = (
            transactions_serializers.request.TransactionCreateRequestSerializer(
                data=request.data
            )
        )
        serializer.is_valid(raise_exception=True)

        # Create transaction
        transaction = transactions_models.Transaction.objects.create(
            branch=serializer.validated_data["branch"],
            cashier=request.user,
            amount_tendered=serializer.validated_data["amount_tendered"],
        )

        # Create transaction products
        transaction_products_data = []
        for transaction_product in serializer.validated_data["transaction_products"]:
            transaction_products_data.append(
                transactions_models.TransactionProduct(
                    transaction=transaction,
                    branch_product=transaction_product["branch_product"],
                    price=transaction_product["price"],
                    quantity=transaction_product["quantity"],
                )
            )
        transactions_models.TransactionProduct.objects.bulk_create(
            transaction_products_data
        )

        # Update quantity into branch product's balance
        for transaction_product in transaction.transaction_products.all():
            branch_product = branches_models.BranchProduct.objects.get(
                pk=transaction_product.branch_product_id
            )
            branch_product.balance -= transaction_product.quantity
            branch_product.save()

            # Check for possible notifications
            branch_product.update_notification()

        # Create response
        response = transactions_serializers.response.TransactionResponseSerializer(
            transaction
        )

        return Response(response.data)

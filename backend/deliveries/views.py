from backend.branches import models as branches_models
from backend.deliveries import globals as deliveries_globals
from backend.deliveries import models as deliveries_models
from backend.deliveries import serializers as deliveries_serializers
from backend.generic.views import BaseViewSet
from backend.users import models as users_models
from backend.users.globals import CLIENT_TYPES
from django.db import transaction
from django.utils import timezone
from drf_yasg.utils import swagger_auto_schema
from rest_framework import filters, mixins
from rest_framework.response import Response


class DeliveryViewSet(
    BaseViewSet,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
):
    queryset = deliveries_models.Delivery.objects
    serializer_class = deliveries_serializers.response.DeliveryResponseSerializer

    # TODO: Apply this way of ordering queryset results: Preorder, Transactions
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ["id"]
    ordering = ["-id"]

    def get_queryset(self):
        queryset = super().get_queryset()
        request = self.request

        serializer = deliveries_serializers.query.DeliveryQuerySerializer(
            data=request.query_params
        )
        serializer.is_valid(raise_exception=True)

        payment_status = serializer.validated_data.get("payment_status", None)
        if payment_status is not None:
            queryset = queryset.with_payment_status(payment_status)

        return queryset.all()

    @swagger_auto_schema(
        query_serializer=deliveries_serializers.query.DeliveryQuerySerializer,
        responses={200: deliveries_serializers.response.DeliveryResponseSerializer},
    )
    def list(self, request, *args, **kwargs):
        """List Deliveries

        Gets a collection of Deliveries.
        """
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        """Retrieve Delivery

        Gets a Delivery.
        """
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        request_body=deliveries_serializers.request.DeliveryCreateRequestSerializer(),
        responses={201: deliveries_serializers.response.DeliveryResponseSerializer},
    )
    @transaction.atomic
    def create(self, request, *args, **kwargs):
        """Create a Delivery

        Create a new Delivery.
        """

        serializer = deliveries_serializers.request.DeliveryCreateRequestSerializer(
            data=request.data
        )
        serializer.is_valid(raise_exception=True)

        # Create or update client
        customer = serializer.validated_data["customer"]
        customer_obj = customer.get("id", None)
        customer_id = customer_obj.id if customer_obj is not None else None
        client, created = users_models.Client.objects.update_or_create(
            pk=customer_id,
            defaults={
                "name": customer["name"],
                "description": customer["description"],
                "address": customer["address"],
                "landline": customer.get("landline", None),
                "phone": customer.get("phone", None),
                "type": CLIENT_TYPES["CUSTOMER"],
                "is_bakery": customer.get("is_bakery", False),
            },
        )

        # Create delivery
        delivery = deliveries_models.Delivery.objects.create(
            branch=serializer.validated_data["branch"],
            user=request.user,
            customer=client,
            delivery_type=serializer.validated_data["delivery_type"],
            status=deliveries_globals.DELIVERY_STATUSES["PENDING"],
            datetime_delivery=serializer.validated_data["datetime_delivery"],
        )

        # Create delivery products
        delivery_products_data = []
        for delivery_product in serializer.validated_data["delivery_products"]:
            delivery_products_data.append(
                deliveries_models.DeliveryProduct(
                    delivery=delivery,
                    branch_product=delivery_product["branch_product"],
                    price=delivery_product["price"],
                    quantity=delivery_product["quantity"],
                )
            )
        deliveries_models.DeliveryProduct.objects.bulk_create(delivery_products_data)

        # Create response
        response = deliveries_serializers.response.DeliveryResponseSerializer(delivery)

        return Response(response.data)

    @swagger_auto_schema(
        request_body=deliveries_serializers.request.DeliveryUpdateRequestSerializer(),
        responses={200: deliveries_serializers.response.DeliveryResponseSerializer()},
    )
    def partial_update(self, request, *args, **kwargs):
        """Update Delivery Partially

        Partially updates a delivery.
        """
        serializer = deliveries_serializers.request.DeliveryUpdateRequestSerializer(
            data=request.data
        )
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data

        # Update delivery
        delivery = self.get_object()

        status = data.get("status", None)
        if status is not None:
            setattr(delivery, "status", status)

            if status == deliveries_globals.DELIVERY_STATUSES["DELIVERED"]:
                setattr(delivery, "datetime_completed", timezone.now())

                for delivery_product in delivery.delivery_products.all():

                    branch_product = branches_models.BranchProduct.objects.get(
                        pk=delivery_product.branch_product_id
                    )
                    branch_product.balance -= delivery_product.quantity
                    branch_product.save()

                    # Check for possible notifications
                    branch_product.update_notification()

        payment_status = data.get("payment_status", None)
        if payment_status is not None:
            setattr(delivery, "payment_status", payment_status)

        prepared_by = data.get("prepared_by", None)
        if prepared_by is not None:
            setattr(delivery, "prepared_by", prepared_by)

        checked_by = data.get("checked_by", None)
        if checked_by is not None:
            setattr(delivery, "checked_by", checked_by)

        pulled_out_by = data.get("pulled_out_by", None)
        if pulled_out_by is not None:
            setattr(delivery, "pulled_out_by", pulled_out_by)

        delivered_by = data.get("delivered_by", None)
        if delivered_by is not None:
            setattr(delivery, "delivered_by", delivered_by)

        delivery.save()

        # Create response
        response = deliveries_serializers.response.DeliveryResponseSerializer(delivery)

        return Response(response.data)

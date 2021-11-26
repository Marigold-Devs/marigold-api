from backend.generic.views import BaseViewSet
from backend.reports import serializers as reports_serializers
from backend.users.globals import CLIENT_TYPES
from rest_framework.response import Response
from rest_framework.decorators import action
from backend.users import models as users_models
from backend.users import globals as users_globals
from backend.products import models as products_models
from drf_yasg.utils import swagger_auto_schema


class ReportViewSet(BaseViewSet):
    queryset = users_models.Client.objects

    def get_queryset(self):
        serializer = reports_serializers.query.ReportsQuerySerializer(
            data=self.request.query_params
        )
        serializer.is_valid(raise_exception=True)

        date_range = serializer.validated_data.get("date_range")

        if self.action == "top_products":
            branch_id = serializer.validated_data.get("branch_id", None)

            return products_models.Product.objects.by_purchases(
                branch_id=branch_id, date_range=date_range
            )

        elif self.action == "top_customers":
            return users_models.Client.objects.with_type(
                type=users_globals.CLIENT_TYPES["CUSTOMER"]
            ).by_purchases(date_range=date_range)

    @swagger_auto_schema(
        query_serializer=reports_serializers.query.ReportsQuerySerializer(),
        responses={200: reports_serializers.response.TopProductsResponseSerializer()},
    )
    @action(url_path="top-products", detail=False, methods=["GET"])
    def top_products(self, request):
        """Get Top Selling Products

        Gets the top selling products from a branch and within date range
        """
        queryset = self.get_queryset().order_by("-total_quantity")

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = reports_serializers.response.TopProductsResponseSerializer(
                page,
                many=True,
            )
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(url_path="top-customers", detail=False, methods=["GET"])
    def top_customers(self, request):
        """Get Top Paying Customers

        Gets the top paying customers from a branch and within date range
        """
        queryset = self.get_queryset().order_by("-total_purchase")

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = reports_serializers.response.TopCustomersResponseSerializer(
                page,
                many=True,
            )
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

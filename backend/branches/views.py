from backend.branches import models as branches_models
from backend.branches import serializers as branches_serializers
from backend.generic.views import BaseViewSet
from backend.products import models as products_models
from drf_yasg.utils import swagger_auto_schema
from rest_framework import filters, mixins
from rest_framework.response import Response


class BranchViewSet(
    BaseViewSet,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
):
    queryset = branches_models.Branch.objects.all()
    serializer_class = branches_serializers.base.BranchesSerializer

    @swagger_auto_schema(
        responses={200: branches_serializers.base.BranchesSerializer()},
    )
    def list(self, request, *args, **kwargs):
        """List Branches

        Gets a collection of Branches.
        """
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        request_body=branches_serializers.request.BranchCreateUpdateRequestSerializer(),
        responses={201: branches_serializers.base.BranchesSerializer()},
    )
    def create(self, request, *args, **kwargs):
        """Create a Branch

        Create a new Branch.
        """

        serializer = branches_serializers.request.BranchCreateUpdateRequestSerializer(
            data=request.data
        )
        serializer.is_valid(raise_exception=True)

        # Create branch
        branch = branches_models.Branch.objects.create(
            name=serializer.validated_data["name"],
        )

        # Create branch products
        branch_products_data = []
        for product_price in products_models.ProductPrice.objects.all():
            branch_products_data.append(
                branches_models.BranchProduct(
                    branch=branch, product_price=product_price
                )
            )
        branches_models.BranchProduct.objects.bulk_create(branch_products_data)

        # Create response
        response = branches_serializers.base.BranchesSerializer(branch)

        return Response(response.data)

    @swagger_auto_schema(
        request_body=branches_serializers.request.BranchCreateUpdateRequestSerializer(),
        responses={200: branches_serializers.base.BranchesSerializer()},
    )
    def partial_update(self, request, *args, **kwargs):
        """Update Branch Partially

        Partially updates a branch.
        """
        serializer = branches_serializers.request.BranchCreateUpdateRequestSerializer(
            data=request.data
        )
        serializer.is_valid(raise_exception=True)

        # Update branch
        branch = self.get_object()
        setattr(branch, "name", serializer.validated_data["name"])
        branch.save()

        # Create response
        response = branches_serializers.base.BranchesSerializer(branch)

        return Response(response.data)

    def destroy(self, request, *args, **kwargs):
        """Delete Branch

        Deletes a branch
        """
        return super().destroy(request, *args, **kwargs)


class BranchProductsViewSet(
    BaseViewSet,
    mixins.ListModelMixin,
):
    queryset = products_models.Product.objects.all()
    serializer_class = branches_serializers.query.BranchProductsQuerySerializer

    @swagger_auto_schema(
        query_serializer=branches_serializers.query.BranchProductsQuerySerializer(),
        responses={
            200: branches_serializers.response.BranchProductsResponseSerializer()
        },
    )
    def list(self, request, *args, **kwargs):
        """List Branch Products

        Gets a collection of Branch Products.
        """

        serializer = branches_serializers.query.BranchProductsQuerySerializer(
            data=request.query_params
        )
        serializer.is_valid(raise_exception=True)

        queryset = products_models.Product.objects.filter(
            name__icontains=serializer.validated_data.get("search", "")
        )

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = branches_serializers.response.BranchProductsResponseSerializer(
                page,
                many=True,
                context={
                    "branch_id": serializer.validated_data.get("branch_id", None),
                    **self.get_serializer_context(),
                },
            )
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

        # products = self.get_queryset()
        # return Response(products.values())

        # return super().list(request, *args, **kwargs)

from backend.branches import models as branches_models
from backend.generic.views import BaseViewSet
from backend.products import models as products_models
from backend.products import serializers as products_serializers
from drf_yasg.utils import swagger_auto_schema
from rest_framework import filters, mixins
from rest_framework.response import Response


class ProductViewSet(
    BaseViewSet,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
):
    queryset = products_models.Product.objects.all()
    serializer_class = products_serializers.response.ProductResponseSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["name"]

    def get_queryset(self):
        queryset = super().get_queryset()
        request = self.request

        serializer = products_serializers.query.ProductsQuerySerializer(
            data=request.query_params
        )
        serializer.is_valid(raise_exception=True)

        ids = serializer.validated_data.get("ids", None)
        if ids:
            queryset = queryset.with_ids(ids)

        return queryset.all()

    @swagger_auto_schema(
        query_serializer=products_serializers.query.ProductsQuerySerializer,
        responses={200: products_serializers.response.ProductResponseSerializer},
    )
    def list(self, request, *args, **kwargs):
        """List Products

        Gets a collection of Products.
        """
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        """Retrieve Product

        Gets a Product.
        """
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        request_body=products_serializers.request.ProductCreateRequestSerializer(),
        responses={201: products_serializers.response.ProductResponseSerializer()},
    )
    def create(self, request, *args, **kwargs):
        """Create a Product

        Create a new Product.
        """

        serializer = products_serializers.request.ProductCreateRequestSerializer(
            data=request.data
        )
        serializer.is_valid(raise_exception=True)

        # Create product
        product = products_models.Product.objects.create(
            name=serializer.validated_data["name"],
            unit_cost=serializer.validated_data["unit_cost"],
            vat_type=serializer.validated_data["vat_type"],
        )

        # Create product prices
        product_prices_data = []
        for product_price in serializer.validated_data["product_prices"]:
            product_prices_data.append(
                products_models.ProductPrice(product=product, **product_price)
            )
        product_prices = products_models.ProductPrice.objects.bulk_create(
            product_prices_data
        )

        # Create branch products
        branches = branches_models.Branch.objects.all()
        product_prices = products_models.ProductPrice.objects.filter(product=product)

        if len(branches) > 0:
            branch_products_data = []
            for branch in branches:
                for product_price in product_prices:
                    branch_products_data.append(
                        branches_models.BranchProduct(
                            branch=branch, product_price=product_price
                        )
                    )

            branches_models.BranchProduct.objects.bulk_create(branch_products_data)

        # Create response
        response = products_serializers.response.ProductResponseSerializer(
            {
                "product_prices": product_prices,
                **products_serializers.base.ProductSerializer(product).data,
            }
        )

        return Response(response.data)

    @swagger_auto_schema(
        request_body=products_serializers.request.ProductUpdateRequestSerializer(),
        responses={200: products_serializers.response.ProductResponseSerializer()},
    )
    def partial_update(self, request, *args, **kwargs):
        """Update Product Partially

        Partially updates a Product.
        """
        serializer = products_serializers.request.ProductUpdateRequestSerializer(
            data=request.data
        )
        serializer.is_valid(raise_exception=True)

        # Update product
        product = self.get_object()
        setattr(product, "name", serializer.validated_data["name"])
        setattr(product, "unit_cost", serializer.validated_data["unit_cost"])
        setattr(product, "vat_type", serializer.validated_data["vat_type"])
        product.save()

        # Update product prices
        product_price_ids = []
        new_product_price_ids = []
        for product_price in serializer.validated_data["product_prices"]:
            item = None
            if "id" in product_price:
                item = products_models.ProductPrice.objects.filter(
                    pk=product_price["id"]
                ).first()
                for (key, value) in product_price.items():
                    setattr(item, key, value)
                item.save()
            else:
                item = products_models.ProductPrice.objects.create(
                    product_id=product.id, **product_price
                )
                new_product_price_ids.append(item.id)

            product_price_ids.append(item.id)

        # Create branch products
        branches = branches_models.Branch.objects.all()

        if len(branches) > 0 and len(new_product_price_ids) > 0:
            branch_products_data = []
            for branch in branches:
                for product_price_id in new_product_price_ids:
                    branch_products_data.append(
                        branches_models.BranchProduct(
                            branch=branch, product_price_id=product_price_id
                        )
                    )

            branches_models.BranchProduct.objects.bulk_create(branch_products_data)

        # Create response
        response = products_serializers.response.ProductResponseSerializer(
            {
                "product_prices": products_models.ProductPrice.objects.filter(
                    id__in=product_price_ids
                ),
                **products_serializers.base.ProductSerializer(product).data,
            }
        )

        return Response(response.data)

    def destroy(self, request, *args, **kwargs):
        """Delete Product

        Deletes a product
        """
        return super().destroy(request, *args, **kwargs)


class UnitTypeViewSet(
    BaseViewSet,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
):
    queryset = products_models.UnitType.objects.all()
    serializer_class = products_serializers.base.UnitTypeSerializer

    filter_backends = [filters.OrderingFilter]
    ordering_fields = ["name"]
    ordering = ["name"]

    def list(self, request, *args, **kwargs):
        """List Unit Types

        Gets a collection of Unit Types.
        """
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        request_body=products_serializers.request.UnitTypeCreateUpdateRequestSerializer(),
        responses={201: products_serializers.base.UnitTypeSerializer()},
    )
    def create(self, request, *args, **kwargs):
        """Create Unit Type

        Create a new Unit Type.
        """
        serializer = products_serializers.request.UnitTypeCreateUpdateRequestSerializer(
            data=request.data
        )
        serializer.is_valid(raise_exception=True)

        unit_type = products_models.UnitType.objects.create(
            name=serializer.validated_data["name"],
        )

        response = products_serializers.base.UnitTypeSerializer(unit_type)

        return Response(response.data)

    def partial_update(self, request, *args, **kwargs):
        """Update Unit Type

        Partially updates a unit type.
        """
        serializer = products_serializers.request.UnitTypeCreateUpdateRequestSerializer(
            data=request.data
        )
        serializer.is_valid(raise_exception=True)

        unit_type = self.get_object()
        setattr(unit_type, "name", serializer.validated_data["name"])
        unit_type.save()

        response = products_serializers.base.UnitTypeSerializer(unit_type)

        return Response(response.data)

from backend.generic.views import BaseViewSet
from backend.products import models as products_models
from backend.products import serializers as products_serializers
from drf_yasg.utils import swagger_auto_schema
from rest_framework import filters, mixins
from rest_framework.response import Response


class ProductViewSet(
    BaseViewSet,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
):
    queryset = products_models.Product.objects.all()
    serializer_class = products_serializers.response.ProductResponseSerializer

    filter_backends = [filters.SearchFilter]
    search_fields = ["name"]

    @swagger_auto_schema(
        request_body=None,
        responses={200: products_serializers.response.ProductResponseSerializer()},
    )
    def list(self, request, *args, **kwargs):
        """List Products

        Gets a collection of Products.
        """
        return super().list(request, *args, **kwargs)

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
                products_models.ProductPrice(product_id=product.id, **product_price)
            )
        product_prices = products_models.ProductPrice.objects.bulk_create(
            product_prices_data
        )

        data = {
            "product_prices": product_prices,
            **products_serializers.base.ProductSerializer(product).data,
        }

        return Response(
            products_serializers.response.ProductResponseSerializer(data).data
        )

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
        for product_price in serializer.validated_data["product_prices"]:
            item = None
            if "id" in product_price:
                item = products_models.ProductPrice.objects.filter(pk=27).first()
                for (key, value) in product_price.items():
                    setattr(item, key, value)
                item.save()
            else:
                item = products_models.ProductPrice.objects.create(
                    product_id=product.id, **product_price
                )

            product_price_ids.append(item.id)

        data = {
            "product_prices": products_models.ProductPrice.objects.filter(
                id__in=product_price_ids
            ),
            **products_serializers.base.ProductSerializer(product).data,
        }

        return Response(
            products_serializers.response.ProductResponseSerializer(data).data
        )

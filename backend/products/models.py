from backend.products import querysets as products_querysets
from backend.products.choices import VAT_TYPE_CHOICES
from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=50)

    unit_cost = models.DecimalField(default=None, max_digits=10, decimal_places=2)

    vat_type = models.CharField(max_length=5, choices=VAT_TYPE_CHOICES)

    objects = products_querysets.ProductQuerySet.as_manager()

    class Meta:
        db_table = "products"

    def __str__(self):
        return "%d - %s" % (self.id, self.name)


class UnitType(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        db_table = "unit_types"

    def __str__(self):
        return "%d - %s" % (self.id, self.name)


class ProductPrice(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="product_prices",
    )

    unit_type = models.ForeignKey(
        UnitType,
        on_delete=models.CASCADE,
        related_name="product_prices",
    )

    price_market = models.DecimalField(
        default=None, blank=True, null=True, max_digits=10, decimal_places=2
    )

    price_delivery = models.DecimalField(
        default=None, blank=True, null=True, max_digits=10, decimal_places=2
    )

    price_pickup = models.DecimalField(
        default=None, blank=True, null=True, max_digits=10, decimal_places=2
    )

    price_special = models.DecimalField(
        default=None, blank=True, null=True, max_digits=10, decimal_places=2
    )

    reorder_point = models.DecimalField(default=0, max_digits=10, decimal_places=3)

    objects = products_querysets.ProductPriceQuerySet.as_manager()

    class Meta:
        db_table = "product_prices"

    def __str__(self):
        return "%d - %s - %s" % (self.id, self.product.name, self.unit_type.name)

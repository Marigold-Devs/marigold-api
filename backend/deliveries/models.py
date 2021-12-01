from backend.branches import models as branch_models
from backend.deliveries import choices as deliveries_choices
from backend.users import models as user_models
from django.db import models
from django.utils import timezone


class Delivery(models.Model):
    branch = models.ForeignKey(
        branch_models.Branch,
        on_delete=models.CASCADE,
        related_name="deliveries",
    )

    user = models.ForeignKey(
        user_models.User,
        on_delete=models.CASCADE,
        related_name="deliveries",
    )

    customer = models.ForeignKey(
        user_models.Client,
        on_delete=models.CASCADE,
        related_name="deliveries",
    )

    delivery_type = models.CharField(
        max_length=20,
        choices=deliveries_choices.DELIVERY_TYPES_CHOICES,
    )

    status = models.CharField(
        max_length=20,
        choices=deliveries_choices.DELIVERY_STATUSES_CHOICES,
    )

    datetime_delivery = models.DateTimeField()

    datetime_completed = models.DateTimeField(null=True, blank=True)

    datetime_created = models.DateTimeField(default=timezone.now)

    prepared_by = models.CharField(max_length=50, blank=True)

    checked_by = models.CharField(max_length=50, blank=True)

    pulled_out_by = models.CharField(max_length=50, blank=True)

    delivered_by = models.CharField(max_length=50, blank=True)

    class Meta:
        db_table = "deliveries"

    def __str__(self):
        return "%d - %s" % (self.id, self.user.name)


class DeliveryProduct(models.Model):
    delivery = models.ForeignKey(
        Delivery,
        on_delete=models.CASCADE,
        related_name="delivery_products",
    )

    branch_product = models.ForeignKey(
        branch_models.BranchProduct,
        on_delete=models.CASCADE,
        related_name="delivery_products",
    )

    price = models.DecimalField(max_digits=10, decimal_places=2)

    quantity = models.DecimalField(default=0, max_digits=10, decimal_places=3)

    class Meta:
        db_table = "delivery_products"

    def __str__(self):
        return "%d - %d - %s" % (
            self.delivery.id,
            self.id,
            self.branch_product.product_price.product.name,
        )

from backend.branches import models as branch_models
from backend.preorders import choices as preorders_choices
from backend.users import models as user_models
from django.db import models
from django.utils import timezone


class Preorder(models.Model):
    branch = models.ForeignKey(
        branch_models.Branch,
        on_delete=models.CASCADE,
        related_name="preorders",
    )

    user = models.ForeignKey(
        user_models.User,
        on_delete=models.CASCADE,
        related_name="preorders",
    )

    supplier = models.ForeignKey(
        user_models.Client,
        on_delete=models.CASCADE,
        related_name="preorders",
    )

    delivery_type = models.CharField(
        max_length=20,
        choices=preorders_choices.DELIVERY_TYPES_CHOICES,
    )

    status = models.CharField(
        max_length=20,
        choices=preorders_choices.PREORDER_STATUSES_CHOICES,
    )

    datetime_created = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "preorders"

    def __str__(self):
        return "%d - %s" % (self.id, self.name)


class PreorderProduct(models.Model):
    preorder = models.ForeignKey(
        Preorder,
        on_delete=models.CASCADE,
        related_name="preorder_products",
    )

    branch_product = models.ForeignKey(
        branch_models.BranchProduct,
        on_delete=models.CASCADE,
        related_name="preorder_products",
    )

    quantity = models.DecimalField(default=0, max_digits=10, decimal_places=3)

    class Meta:
        db_table = "preorder_products"

    def __str__(self):
        return "%d - %d - %s" % (
            self.preorder.id,
            self.id,
            self.branch_product.product_price.product.name,
        )


class PreorderTransaction(models.Model):
    preorder = models.ForeignKey(
        Preorder,
        on_delete=models.CASCADE,
        related_name="preorder_transactions",
    )

    user = models.ForeignKey(
        user_models.User,
        on_delete=models.CASCADE,
        related_name="preorder_transactions",
    )

    class Meta:
        db_table = "preorder_transactions"

    def __str__(self):
        return "%d - %d - %s %s" % (
            self.preorder.id,
            self.id,
            self.user.first_name,
            self.user.last_name,
        )


class PreorderTransactionProduct(models.Model):
    preorder_transaction = models.ForeignKey(
        PreorderTransaction,
        on_delete=models.CASCADE,
        related_name="preorder_transaction_products",
    )

    preorder_product = models.ForeignKey(
        PreorderProduct,
        on_delete=models.CASCADE,
        related_name="preorder_transaction_products",
    )

    quantity = models.DecimalField(default=0, max_digits=10, decimal_places=3)

    class Meta:
        db_table = "preorder_transaction_products"

    def __str__(self):
        return "%d - %d - %s %s" % (
            self.preorder.id,
            self.id,
            self.user.first_name,
            self.user.last_name,
        )

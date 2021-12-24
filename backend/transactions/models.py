from backend.branches import models as branch_models
from backend.users import models as user_models
from django.db import models
from django.utils import timezone


class Transaction(models.Model):
    branch = models.ForeignKey(
        branch_models.Branch,
        on_delete=models.CASCADE,
        related_name="transactions",
    )

    cashier = models.ForeignKey(
        user_models.User,
        on_delete=models.CASCADE,
        related_name="transactions",
    )

    amount_tendered = models.DecimalField(max_digits=10, decimal_places=2)

    datetime_created = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "transactions"

    def __str__(self):
        return "%d - %s" % (self.id, self.cashier.first_name)


class TransactionProduct(models.Model):
    transaction = models.ForeignKey(
        Transaction,
        on_delete=models.CASCADE,
        related_name="transaction_products",
    )

    branch_product = models.ForeignKey(
        branch_models.BranchProduct,
        on_delete=models.CASCADE,
        related_name="transaction_products",
    )

    price = models.DecimalField(max_digits=10, decimal_places=2)

    quantity = models.DecimalField(default=0, max_digits=10, decimal_places=3)

    class Meta:
        db_table = "transaction_products"

    def __str__(self):
        return "%d - %d - %s" % (
            self.transaction.id,
            self.id,
            self.branch_product.product_price.product.name,
        )

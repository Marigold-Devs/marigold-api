from backend.products import models as products_models
from backend.branches import globals as branches_globals

from django.db import models


class Branch(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        db_table = "branches"

    def __str__(self):
        return "%d - %s" % (self.id, self.name)


class BranchProduct(models.Model):
    branch = models.ForeignKey(
        Branch,
        on_delete=models.CASCADE,
        related_name="branch_products",
    )
    product_price = models.ForeignKey(
        products_models.ProductPrice,
        on_delete=models.CASCADE,
        related_name="branch_products",
    )

    balance = models.DecimalField(default=0, max_digits=10, decimal_places=3)

    class Meta:
        db_table = "branch_products"

    def get_status(self):
        status = None
        balance = self.balance
        reorder_point = self.product_price.reorder_point

        if balance == 0:
            status = branches_globals.BRANCH_PRODUCT_STATUSES["OUT_OF_STOCK"]
        elif balance <= reorder_point:
            status = branches_globals.BRANCH_PRODUCT_STATUSES["REORDER"]

        return status

    def update_notification(self):
        from backend.notifications import models as notifications_models

        status = self.get_status()
        statuses_needed_action = [
            branches_globals.BRANCH_PRODUCT_STATUSES["OUT_OF_STOCK"],
            branches_globals.BRANCH_PRODUCT_STATUSES["REORDER"],
        ]

        if status in statuses_needed_action:
            notifications_models.Notification.objects.create(branch_product=self)
        else:
            notifications_models.Notification.objects.filter(
                branch_product=self
            ).delete()

    def __str__(self):
        return "%d - %s - %s" % (
            self.id,
            self.branch.name,
            self.product_price.product.name,
        )

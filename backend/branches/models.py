from django.db import models
from backend.products import models as product_models
from backend.branches import querysets as branches_querysets


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
        product_models.ProductPrice,
        on_delete=models.CASCADE,
        related_name="branch_products",
    )

    balance = models.DecimalField(default=0, max_digits=10, decimal_places=3)

    class Meta:
        db_table = "branch_products"

    objects = branches_querysets.BranchProductQuerySet.as_manager()

    def __str__(self):
        return "%d - %s - %s" % (
            self.id,
            self.branch.name,
            self.product_price.product.name,
        )

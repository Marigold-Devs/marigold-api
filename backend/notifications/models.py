from backend.branches import models as branch_models
from backend.notifications.querysets import NotificationQuerySet
from django.db import models


class Notification(models.Model):
    branch_product = models.ForeignKey(
        branch_models.BranchProduct,
        on_delete=models.CASCADE,
        related_name="notifications",
    )

    objects = NotificationQuerySet.as_manager()

    class Meta:
        db_table = "notifications"

    def __str__(self):
        return "%d - %s - %s" % (
            self.id,
            self.branch.name,
            self.product_price.product.name,
        )

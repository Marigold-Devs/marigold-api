import calendar

from django.utils import timezone
from django.db.models import QuerySet, Q, F, Sum, OuterRef, Prefetch, Count
from django.db.models.expressions import Case, When
from django.db.models.fields import CharField, DecimalField, IntegerField
from django.db.models.expressions import Case, Subquery, When
from django.db.models.functions import Coalesce
from backend.products import models as products_models
from backend.branches import models as branches_models

from backend.branches import globals as branches_globals


class ProductQuerySet(QuerySet):
    def with_name(self, name: str):
        return self.filter(name__icontains=name)

    def with_product_status(self, branch_id: int, product_status: str):
        product_status_val = None

        if product_status == branches_globals.BRANCH_PRODUCT_STATUSES["AVAILABLE"]:
            product_status_val = 1
        elif product_status == branches_globals.BRANCH_PRODUCT_STATUSES["OUT_OF_STOCK"]:
            product_status_val = 2
        elif product_status == branches_globals.BRANCH_PRODUCT_STATUSES["REORDER"]:
            product_status_val = 3
        else:
            # if the product_status is invalid,
            # return the unfiltered queryset immediately
            return self

        return (
            self.annotate(
                total_branch_product_balance=Sum(
                    "product_prices__branch_products__balance"
                )
            )
            .annotate(
                reorder_count=Count(
                    "pk",
                    filter=Q(product_prices__branch_products__branch_id=branch_id)
                    & ~Q(product_prices__reorder_point__exact=0)
                    & Q(
                        product_prices__reorder_point__gte=F(
                            "product_prices__branch_products__balance"
                        )
                    ),
                    distinct=True,
                )
            )
            .annotate(
                product_status=Case(
                    When(
                        ~Q(product_prices__branch_products__branch_id=branch_id),
                        then=0,
                    ),
                    When(
                        Q(total_branch_product_balance=0),
                        then=2,
                    ),
                    When(
                        Q(reorder_count__gt=0),
                        then=3,
                    ),
                    default=1,
                    output_field=IntegerField(),
                )
            )
            .filter(product_status=product_status_val)
        )

import calendar

from backend.branches import globals as branches_globals
from backend.deliveries import globals as deliveries_globals
from django.db.models import Count, F, Q, QuerySet, Sum
from django.db.models.expressions import Case, Value, When
from django.db.models.fields import DecimalField, IntegerField
from django.db.models.functions import Coalesce
from django.utils import timezone


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

    def by_purchases(self, branch_id: int, date_range: str):
        branch_id_value = -1 if branch_id is None else branch_id
        start_date = timezone.now().replace(hour=0, minute=0, second=0)
        end_date = timezone.now().replace(hour=23, minute=59, second=59)

        if date_range == "daily":
            start_date = timezone.now().replace(hour=0, minute=0, second=0)
            end_date = timezone.now().replace(hour=23, minute=59, second=59)

        elif date_range == "monthly":
            last_day = calendar.monthrange(
                timezone.now().today().year, timezone.now().today().month
            )[1]
            start_date = timezone.now().replace(day=1, hour=0, minute=0, second=0)
            end_date = timezone.now().replace(
                day=last_day, hour=23, minute=59, second=59
            )

        else:
            start_date, end_date = date_range.split(",")
            start_date = timezone.datetime.strptime(start_date, "%m/%d/%y").replace(
                hour=0, minute=0, second=0
            )
            end_date = timezone.datetime.strptime(end_date, "%m/%d/%y").replace(
                hour=23, minute=59, second=59
            )

        return self.annotate(branch_id_value=Value(branch_id_value)).annotate(
            total_quantity=Coalesce(
                Sum(
                    Case(
                        When(
                            Q(
                                product_prices__branch_products__delivery_products__delivery__datetime_created__gte=start_date
                            )
                            & Q(
                                product_prices__branch_products__delivery_products__delivery__datetime_created__lte=end_date
                            )
                            & Q(
                                product_prices__branch_products__delivery_products__delivery__status__icontains=deliveries_globals.DELIVERY_STATUSES[
                                    "DELIVERED"
                                ]
                            )
                            & (
                                Q(branch_id_value=-1)
                                | Q(
                                    product_prices__branch_products__branch_id=branch_id_value
                                )
                            ),
                            then=F(
                                "product_prices__branch_products__delivery_products__quantity"
                            ),
                        ),
                        default=0.0,
                        output_field=DecimalField(),
                    ),
                ),
                0,
                output_field=DecimalField(),
            )
        )

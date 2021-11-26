import calendar

from backend.deliveries import globals as deliveries_globals
from django.db.models import F, Q, QuerySet, Sum
from django.db.models.expressions import Case, When
from django.db.models.fields import DecimalField
from django.db.models.functions import Coalesce
from django.utils import timezone


class UserQuerySet(QuerySet):
    def id(self, id: int):
        return self.filter(id=id)

    def has_no_admin(self):
        return self.filter(~Q(id=1))

    def has_username(self, username: str):
        return self.filter(username=username)

    def has_email(self, email: str):
        return self.filter(email__iexact=email)

    def with_type(self, user_type: str):
        return self.filter(user_type=user_type)


class ClientQuerySet(QuerySet):
    def with_type(self, type: str):
        if type is None:
            return self

        return self.filter(type=type)

    def by_purchases(self, date_range: str):
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

        return self.annotate(
            total_purchase=Coalesce(
                Sum(
                    Case(
                        When(
                            Q(deliveries__datetime_created__gte=start_date)
                            & Q(deliveries__datetime_created__lte=end_date)
                            & Q(
                                deliveries__status__icontains=deliveries_globals.DELIVERY_STATUSES[
                                    "DELIVERED"
                                ]
                            ),
                            then=F("deliveries__delivery_products__quantity")
                            * F("deliveries__delivery_products__price"),
                        ),
                        default=0,
                        output_field=DecimalField(),
                    ),
                ),
                0,
                output_field=DecimalField(),
            )
        )

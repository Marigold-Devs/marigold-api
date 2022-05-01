from datetime import date
from django.db.models import QuerySet
from django.utils import timezone


class PreorderQuerySet(QuerySet):
    def with_date_created(self, datetime_created: date):
        date = timezone.datetime.strptime(str(datetime_created), "%Y-%m-%d")

        return self.filter(
            datetime_created__gte=date.replace(hour=0, minute=0, second=0),
            datetime_created__lte=date.replace(hour=23, minute=59, second=59),
        )

    def with_date_fulfilled(self, datetime_fulfilled: str):
        date = timezone.datetime.strptime(str(datetime_fulfilled), "%Y-%m-%d")

        return self.filter(
            datetime_fulfilled__gte=date.replace(hour=0, minute=0, second=0),
            datetime_fulfilled__lte=date.replace(hour=23, minute=59, second=59),
        )

    def with_id(self, id: str):
        return self.filter(id__icontains=id)

    def with_supplier_name(self, supplier_name: str):
        return self.filter(supplier__name__icontains=supplier_name)

    def with_status(self, status: str):
        return self.filter(status=status)

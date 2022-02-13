from django.db.models import QuerySet


class DeliveryQuerySet(QuerySet):
    def with_payment_status(self, payment_status: str):
        return self.filter(payment_status=payment_status)

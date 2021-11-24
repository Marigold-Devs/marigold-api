from django.db.models import QuerySet


class NotificationQuerySet(QuerySet):
    def with_branch(self, branch_id: int):
        if branch_id is None:
            return self

        return self.filter(branch_product__branch_id=branch_id)

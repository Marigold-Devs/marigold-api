from django.db.models import QuerySet


class BranchProductQuerySet(QuerySet):
    def of_branch(self, branch_id):
        return self.filter(branch_id=branch_id) if branch_id else self

    def of_product_price(self, product_price_id):
        return (
            self.filter(product_price_id=product_price_id) if product_price_id else self
        )

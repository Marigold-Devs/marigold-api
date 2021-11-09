import datetime

from django.utils import timezone
from django.db.models import QuerySet, Q


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

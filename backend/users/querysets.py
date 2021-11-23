from django.db.models import Q, QuerySet


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

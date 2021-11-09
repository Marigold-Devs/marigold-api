from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone

from .choices import USER_TYPE_CHOICES
from .managers import UserManager
from .querysets import UserQuerySet


class User(AbstractBaseUser, PermissionsMixin):
    # superuser info
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    # authentication fields
    username = models.CharField(max_length=20, unique=True)

    # other fields
    first_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30, blank=True, null=True)
    user_type = models.CharField(
        max_length=20, choices=USER_TYPE_CHOICES, default=None, blank=True, null=True
    )

    objects = UserManager.from_queryset(UserQuerySet)()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["password"]

    @property
    def full_name(self):
        return "%d - %s" % (
            self.id,
            " ".join(
                [
                    "(%s) " % self.username,
                    self.first_name if self.first_name else "",
                    self.last_name if self.last_name else "",
                ]
            ),
        )

    class Meta:
        db_table = "users"

    def __str__(self):
        return "".join(
            [
                str(self.id),
                " - ",
                self.username,
                " - ",
                self.first_name if self.first_name is not None else "",
                " ",
                self.last_name if self.last_name is not None else "",
            ]
        )

from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def get_queryset(self):
        return super().get_queryset()

    def create_user(self, username, user_type, password=None, **other_fields):
        """Creates and returns a new User."""
        user = self._create_user(username, password, **other_fields)
        user.save(using=self._db)

        return user

    def create_superuser(self, username, password, **other_fields):
        user = self._create_user(username, password, **other_fields)

        user.is_staff = True
        user.is_superuser = True

        user.save(using=self._db)

        return user

    def _create_user(self, username, password, **other_fields):

        user = self.model(username=username, **other_fields)
        user.set_password(password)

        return user

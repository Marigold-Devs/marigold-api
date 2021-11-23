from .globals import CLIENT_TYPES, USER_TYPES

USER_TYPE_CHOICES = (
    (USER_TYPES["ADMIN"], "Admin"),
    (USER_TYPES["MANAGER"], "Manager"),
    (USER_TYPES["PERSONNEL"], "Personnel"),
)

CLIENT_TYPE_CHOICES = (
    (CLIENT_TYPES["SUPPLIER"], "supplier"),
    (CLIENT_TYPES["CUSTOMER"], "customer"),
)

from .globals import DELIVERY_STATUSES, DELIVERY_TYPES, PAYMENT_STATUSES

DELIVERY_STATUSES_CHOICES = (
    (DELIVERY_STATUSES["PENDING"], DELIVERY_STATUSES["PENDING"]),
    (DELIVERY_STATUSES["DELIVERED"], DELIVERY_STATUSES["DELIVERED"]),
    (DELIVERY_STATUSES["CANCELLED"], DELIVERY_STATUSES["CANCELLED"]),
)

DELIVERY_TYPES_CHOICES = (
    (DELIVERY_TYPES["MARKET"], DELIVERY_TYPES["MARKET"]),
    (DELIVERY_TYPES["DELIVERY"], DELIVERY_TYPES["DELIVERY"]),
    (DELIVERY_TYPES["PICKUP"], DELIVERY_TYPES["PICKUP"]),
    (DELIVERY_TYPES["SPECIAL"], DELIVERY_TYPES["SPECIAL"]),
)

PAYMENT_STATUSES_CHOICES = (
    (PAYMENT_STATUSES["UNPAID"], PAYMENT_STATUSES["UNPAID"]),
    (PAYMENT_STATUSES["PAID"], PAYMENT_STATUSES["PAID"]),
)

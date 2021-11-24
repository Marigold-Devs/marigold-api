from backend.deliveries import views
from backend.routers import SuppressedPutRouter

ROUTER = SuppressedPutRouter()

ROUTER.register_api("deliveries", views.DeliveryViewSet)

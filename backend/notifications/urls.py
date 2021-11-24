from backend.notifications import views
from backend.routers import SuppressedPutRouter

ROUTER = SuppressedPutRouter()

ROUTER.register_api("notifications", views.NotificationsViewSet)

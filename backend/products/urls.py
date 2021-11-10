from backend.products import views
from backend.routers import SuppressedPutRouter

ROUTER = SuppressedPutRouter()

ROUTER.register_api("products", views.ProductViewSet)

from backend.preorders import views
from backend.routers import SuppressedPutRouter

ROUTER = SuppressedPutRouter()

ROUTER.register_api("preorders", views.PreorderViewSet)
ROUTER.register_api("preorder-transactions", views.PreorderTransactionViewSet)

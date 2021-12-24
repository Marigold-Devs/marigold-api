from backend.transactions import views
from backend.routers import SuppressedPutRouter

ROUTER = SuppressedPutRouter()

ROUTER.register_api("transactions", views.TransactionViewSet)

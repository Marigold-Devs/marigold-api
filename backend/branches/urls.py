from backend.branches import views
from backend.routers import SuppressedPutRouter

ROUTER = SuppressedPutRouter()

ROUTER.register_api("branches", views.BranchViewSet)
ROUTER.register_api("branch-products", views.BranchProductViewSet)

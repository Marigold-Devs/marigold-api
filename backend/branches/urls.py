from backend.routers import SuppressedPutRouter, get_api_route

from backend.branches import views

ROUTER = SuppressedPutRouter()

ROUTER.register_api("branches", views.BranchViewSet)

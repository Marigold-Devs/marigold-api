from django.views.generic import base
from backend.reports import views
from backend.routers import SuppressedPutRouter

ROUTER = SuppressedPutRouter()

ROUTER.register_api("reports", views.ReportViewSet)

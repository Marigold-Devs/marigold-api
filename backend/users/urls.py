from django.urls import re_path

from backend.routers import SuppressedPutRouter, get_api_route
from backend.users import views

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)


ROUTER = SuppressedPutRouter()

ROUTER.register_api("users", views.UserViewSet)

URLS = [
    re_path(
        get_api_route("tokens/acquire/"),
        TokenObtainPairView.as_view(),
        name="token_obtain_pair",
    ),
    re_path(
        get_api_route("tokens/renew/"), TokenRefreshView.as_view(), name="token_refresh"
    ),
    re_path(
        get_api_route("tokens/access/verify/"),
        TokenVerifyView.as_view(),
        name="token_verify",
    ),
]

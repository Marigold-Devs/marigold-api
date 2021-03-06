from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from backend.branches.urls import ROUTER as BRANCHES_ROUTER
from backend.deliveries.urls import ROUTER as DELIVERIES_ROUTER
from backend.notifications.urls import ROUTER as NOTIFICATIONS_ROUTER
from backend.preorders.urls import ROUTER as PREORDERS_ROUTER
from backend.products.urls import ROUTER as PRODUCTS_ROUTER
from backend.reports.urls import ROUTER as REPORTS_ROUTER
from backend.settings import DEV, ENV_TYPE, STATIC_ROOT, STATIC_URL
from backend.transactions.urls import ROUTER as TRANSACTIONS_ROUTER
from backend.users.urls import ROUTER as USERS_ROUTER
from backend.users.urls import URLS as USERS_URLS

urlpatterns = []

# Functional URLs #
# These URLs should come before the ViewSet Routers.
urlpatterns.extend(USERS_URLS)

urlpatterns += [
    url(r"^admin/*/", admin.site.urls),
    url(r"^", include(BRANCHES_ROUTER.urls)),
    url(r"^", include(DELIVERIES_ROUTER.urls)),
    url(r"^", include(NOTIFICATIONS_ROUTER.urls)),
    url(r"^", include(PREORDERS_ROUTER.urls)),
    url(r"^", include(PRODUCTS_ROUTER.urls)),
    url(r"^", include(REPORTS_ROUTER.urls)),
    url(r"^", include(TRANSACTIONS_ROUTER.urls)),
    url(r"^", include(USERS_ROUTER.urls)),
]


### Optional URLs ###

if ENV_TYPE == DEV:
    from django.urls import path
    from django.views.generic import TemplateView

    schema_view = get_schema_view(
        openapi.Info(
            title="Marigold API",
            default_version="v1",
            license=openapi.License(name="BSD License"),
        ),
        public=True,
        permission_classes=(permissions.AllowAny,),
    )
    urlpatterns.append(
        url(
            r"^swagger(?P<format>\.json|\.yaml)$",
            schema_view.without_ui(cache_timeout=0),
            name="schema-json",
        ),
    )
    urlpatterns.append(
        path(
            "docs/",
            TemplateView.as_view(
                template_name="redoc.html",
                extra_context={"schema_url": "openapi-schema"},
            ),
            name="redoc",
        )
    )

    urlpatterns += static(STATIC_URL, document_root=STATIC_ROOT)

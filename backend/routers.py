""" """
from rest_framework.routers import DefaultRouter

from backend.settings import API_VERSION


class DefaultAPIRouter(DefaultRouter):
    """ """

    API_BASE = r"v"

    def register_api(self, prefix, viewset, version=API_VERSION):
        """ """
        route = get_api_route(prefix, version)
        super(DefaultAPIRouter, self).register(route, viewset)


class SuppressedPutRouter(DefaultAPIRouter):
    """
    Router class that disables the PUT method.
    """

    def get_method_map(self, viewset, method_map):

        bound_methods = super().get_method_map(viewset, method_map)

        if "put" in bound_methods.keys():
            del bound_methods["put"]

        return bound_methods


def get_api_route(prefix, version=API_VERSION):
    """ """
    return "".join([DefaultAPIRouter.API_BASE, str(version), r"/", prefix])


class DatabaseRouter(object):
    route_app_labels = {
        "adjustment_slips",
        "delivery_receipts",
        "order_slips",
        "requisition_slips",
        "branches",
        "online_users",
        "online_products",
        "database_transactions",
        "logs",
        "return_item_slips",
        "back_orders",
    }

    def db_for_read(self, model, **hints):
        """
        Attempts to read auth and contenttypes models go to online.
        """
        if model._meta.app_label in self.route_app_labels:
            return "online"
        return None

    def db_for_write(self, model, **hints):
        """
        Attempts to write auth and contenttypes models go to online.
        """
        if model._meta.app_label in self.route_app_labels:
            return "online"
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the auth or contenttypes apps is
        involved.
        """
        if (
            obj1._meta.app_label in self.route_app_labels
            or obj2._meta.app_label in self.route_app_labels
        ):
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Make sure the auth and contenttypes apps only appear in the
        'online' database.
        """
        if app_label in self.route_app_labels:
            return db == "online"
        return None

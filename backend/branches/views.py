# import requests
# import json

# from django.utils import timezone
# from django.db import transaction
# from rest_framework import mixins, serializers, status
# from rest_framework.decorators import action
# from rest_framework.response import Response
# from drf_yasg.utils import swagger_auto_schema

# from backend.generic.encoders import DecimalEncoder
# from backend.generic.views import BaseViewSet

# from backend.branches import (
#     models as branches_models,
#     serializers as branches_serializers,
# )
# from backend.products import models as online_products_models
# from backend.online_products import models as online_products_models
# from backend.database_transactions import (
#     models as database_transactions_models,
#     globals as database_transactions_globals,
#     serializers as database_transactions_serializers,
# )


# class BranchViewSet(
#     mixins.ListModelMixin,
#     mixins.UpdateModelMixin,
#     mixins.CreateModelMixin,
#     mixins.RetrieveModelMixin,
#     mixins.DestroyModelMixin,
#     BaseViewSet,
# ):
#     queryset = branches_models.Branch.objects.has_no_hidden()
#     serializer_class = branches_serializers.base.BranchSerializer

#     def get_queryset(self):
#         queryset = self.queryset

#         return queryset.all()

#     def list(self, request, *args, **kwargs):
#         """List Branches

#         Gets a collection of Branches.
#         """
#         return super().list(request, *args, **kwargs)

#     @swagger_auto_schema(
#         request_body=branches_serializers.request.BranchCreateRequestSerializer(),
#         responses={200: branches_serializers.response.CreateBranchSerializer()},
#     )
#     @transaction.atomic
#     def create(self, request, *args, **kwargs):
#         """Create a Branch

#         Create a new Branch.
#         """
#         serializer = branches_serializers.request.BranchCreateRequestSerializer(
#             data=request.data
#         )
#         serializer.is_valid(raise_exception=True)

#         branch_online_url = serializer.validated_data["online_url"]

#         # before doing anything else, check if we can establish a connection
#         # to the branch's online URL
#         url = "%s/local-branches-settings/" % branch_online_url
#         try:
#             headers = {
#                 "Content-type": "application/json",
#                 "User-Agent": "Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0",
#             }
#             response = requests.get(url, headers=headers, timeout=5,)

#             response.raise_for_status()
#         except Exception as e:
#             return Response(
#                 "Failed to establish a connection to the branch's online URL",
#                 status=status.HTTP_400_BAD_REQUEST,
#             )

#         # if the test request above passes, proceed with the actual process

#         branch = branches_models.Branch.objects.create(**serializer.validated_data)

#         pending_database_transactions = []

#         headers = {
#             "content-type": "application/json",
#             "User-Agent": "Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0",
#         }

#         # create Products
#         for online_product in online_products_models.OnlineProduct.objects.all():
#             create_url = "%s/products/" % branch_online_url
#             product_data = {
#                 "id": online_product.id,
#                 "barcode": online_product.barcode,
#                 "textcode": online_product.textcode,
#                 "name": online_product.name,
#                 "type": online_product.type,
#                 "is_vat_exempted": online_product.is_vat_exempted,
#                 "unit_of_measurement": online_product.unit_of_measurement,
#                 "print_details": online_product.print_details,
#                 "description": online_product.description,
#                 "allowable_spoilage": online_product.allowable_spoilage,
#                 "cost_per_piece": online_product.cost_per_piece,
#                 "cost_per_bulk": online_product.cost_per_bulk,
#                 "pieces_in_bulk": online_product.pieces_in_bulk,
#                 "reorder_point": online_product.reorder_point,
#                 "max_balance": online_product.max_balance,
#                 "price_per_piece": online_product.price_per_piece,
#                 "price_per_bulk": online_product.price_per_bulk,
#             }
#             try:
#                 response = requests.post(
#                     create_url,
#                     data=json.dumps(product_data, cls=DecimalEncoder,),
#                     headers=headers,
#                     timeout=5,
#                 )
#                 response.raise_for_status()
#             except Exception as e:
#                 print(str(e))
#                 pending_database_transactions.append(
#                     database_transactions_models.PendingDatabaseTransaction.objects.create(
#                         branch=branch,
#                         request_model=database_transactions_globals.REQUEST_MODELS[
#                             "PRODUCTS"
#                         ],
#                         name="Create product %s in branch %s"
#                         % (online_product.name, branch.name),
#                         url=create_url,
#                         request_type=database_transactions_globals.REQUEST_TYPES[
#                             "POST"
#                         ],
#                         request_query_params="",
#                         request_body=json.dumps(product_data, cls=DecimalEncoder,),
#                     )
#                 )

#         # create LocalBranchSettings
#         create_url = "%s/local-branches-settings/" % branch_online_url
#         try:
#             response = requests.post(create_url, headers=headers, timeout=5,)
#             response.raise_for_status()
#         except Exception as e:
#             print(str(e))
#             pending_database_transactions.append(
#                 database_transactions_models.PendingDatabaseTransaction.objects.create(
#                     branch=branch,
#                     request_model=database_transactions_globals.REQUEST_MODELS[
#                         "BRANCH_ITEMS"
#                     ],
#                     name="Create local branch settings in branch",
#                     url=create_url,
#                     request_type=database_transactions_globals.REQUEST_TYPES["POST"],
#                     request_query_params="",
#                     request_body=None,
#                 )
#             )

#         # create SiteSettings
#         create_url = "%s/site-settings/" % branch_online_url
#         try:
#             response = requests.post(create_url, headers=headers, timeout=5,)
#             response.raise_for_status()
#         except Exception as e:
#             print(str(e))
#             pending_database_transactions.append(
#                 database_transactions_models.PendingDatabaseTransaction.objects.create(
#                     branch=branch,
#                     request_model=database_transactions_globals.REQUEST_MODELS[
#                         "SITE_SETTINGS"
#                     ],
#                     name="Create site settings in branch",
#                     url=create_url,
#                     request_type=database_transactions_globals.REQUEST_TYPES["POST"],
#                     request_query_params="",
#                     request_body=None,
#                 )
#             )

#         return Response(
#             branches_serializers.response.CreateBranchSerializer(
#                 {
#                     "branch": branch,
#                     "pending_database_transactions": pending_database_transactions,
#                 },
#             ).data
#         )

#     @swagger_auto_schema(
#         request_body=branches_serializers.request.BranchUpdateRequestSerializer(),
#         responses={200: branches_serializers.base.BranchSerializer()},
#     )
#     def partial_update(self, request, *args, **kwargs):
#         """Update Branch Partially

#         Partially updates a Branch.
#         """
#         return super().partial_update(request, *args, **kwargs)

#     def destroy(self, request, *args, **kwargs):
#         """Delete Branch

#         Deletes a Branch with the same `id` in the path parameter.
#         """
#         return super().destroy(request, *args, **kwargs)

#     @swagger_auto_schema(responses={200: branches_serializers.base.BranchSerializer()},)
#     def retrieve(self, request, *args, **kwargs):
#         """
#         Retrieve a Branch

#         Get a Branch with the same `id` in the path parameter.
#         """
#         return super().retrieve(request, *args, **kwargs)

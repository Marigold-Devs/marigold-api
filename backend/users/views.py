from backend.generic.swagger import STRING_RESPONSE
from backend.generic.views import BaseViewSet
from backend.users import models as users_models
from backend.users import serializers as users_serializers
from drf_yasg.utils import swagger_auto_schema
from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response


class UserViewSet(
    BaseViewSet,
    mixins.CreateModelMixin,
):
    queryset = users_models.User.objects.has_no_admin()
    serializer_class = users_serializers.base.UserSerializer
    permission_classes = []

    @swagger_auto_schema(
        request_body=users_serializers.request.UserCreateRequestSerializer(),
        responses={200: users_serializers.base.UserSerializer()},
    )
    def create(self, request, *args, **kwargs):
        """Create a User

        Create a new User.
        """
        serializer = users_serializers.request.UserCreateRequestSerializer(
            data=request.data
        )
        serializer.is_valid(raise_exception=True)
        user = users_models.User.objects.create(**serializer.validated_data)
        user.set_password(serializer.validated_data["password"])
        user.save()

        return Response(users_serializers.base.UserSerializer(user).data)

    @swagger_auto_schema(
        request_body=users_serializers.request.LoginRequestSerializer(),
        responses={
            200: users_serializers.base.UserSerializer(),
            400: STRING_RESPONSE,
            401: STRING_RESPONSE,
        },
    )
    @action(detail=False, methods=["POST"], permission_classes=[])
    def login(self, request):
        """
        Login User

        Login as a user.
        """
        serializer = users_serializers.request.LoginRequestSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user = serializer.validated_data.get("user", None)
        password = serializer.validated_data.get("password", None)

        if not user or not user.check_password(password):
            return Response(
                "Username, email, or password is invalid.",
                status=status.HTTP_401_UNAUTHORIZED,
            )

        return Response(users_serializers.base.UserSerializer(user).data)


class ClientViewSet(
    BaseViewSet,
    mixins.ListModelMixin,
):
    pagination_class = None
    queryset = users_models.Client.objects

    @swagger_auto_schema(
        query_serializer=users_serializers.query.ClientQuerySerializer(),
        responses={200: users_serializers.base.ClientSerializer()},
    )
    def list(self, request, *args, **kwargs):
        """List Clients

        Gets a collection of Clients.
        """

        serializer = users_serializers.query.ClientQuerySerializer(
            data=request.query_params
        )
        serializer.is_valid(raise_exception=True)

        # Query
        queryset = users_models.Client.objects.with_type(
            serializer.validated_data.get("type", None)
        )

        # Create response
        response = users_serializers.base.ClientSerializer(queryset, many=True)

        return Response(response.data)

from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from common.serializers import CreateUserSerializer, RegistrationResponseSerializer

UserModel = get_user_model()


@extend_schema(
    tags=['Auth API'],
    request=CreateUserSerializer,
    responses={'201': RegistrationResponseSerializer})
class RegistrationView(CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = CreateUserSerializer

    def create(self, request, *args, **kwargs):
        user_response = super().create(request, *args, **kwargs)

        if user_response.status_code == 201:
            user = user_response.data.serializer.instance
            refresh = RefreshToken.for_user(user)
            serializer = RegistrationResponseSerializer({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'username': user.username,
                'id': user.id
            })

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return user_response

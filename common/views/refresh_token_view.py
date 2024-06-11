from drf_spectacular.utils import extend_schema
from rest_framework_simplejwt.views import TokenRefreshView


@extend_schema(tags=['Auth API'])
class RefreshTokenView(TokenRefreshView):
    ...

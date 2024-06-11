from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

from common.views import RegistrationView, AccessTokenView, RefreshTokenView

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/v1/', include('products.urls', 'products'), name='products'),
    path('api/v1/', include('orders.urls', 'orders'), name='orders'),
    path('api/v1/', include('analytics.urls', 'analytics'), name='analytics'),

    path('api/v1/auth/registration/', RegistrationView.as_view(), name='registration'),
    path('api/v1/auth/token/', AccessTokenView.as_view(), name='token_obtain_pair'),
    path('api/v1/auth/token/refresh/', RefreshTokenView.as_view(), name='token_refresh'),

    path('api/v1/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/v1/schema/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/v1.schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]

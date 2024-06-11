from django.urls import include, path
from rest_framework import routers

from orders.viewsets import OrderViewSet

app_name = 'orders'

order_router = routers.DefaultRouter()
order_router.register(r'orders', OrderViewSet, basename='orders')

urlpatterns = [
    path(r'', include(order_router.urls)),
]

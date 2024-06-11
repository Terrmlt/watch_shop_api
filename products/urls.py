from django.urls import include, path
from rest_framework import routers

from products.viewsets import ProductsViewSet

app_name = 'products'

router = routers.DefaultRouter()
router.register(r'products', ProductsViewSet, basename='products')

urlpatterns = [
    path('', include(router.urls)),
]

from drf_spectacular.utils import extend_schema
from rest_framework import viewsets

from common.permissions import IsManager, ReadOnly
from products.models import Product
from products.serializers import ProductSerializer, CreateOrUpdateProductSerializer


@extend_schema(tags=['Products API'])
class ProductsViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    permission_classes = [IsManager | ReadOnly]

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return ProductSerializer

        return CreateOrUpdateProductSerializer

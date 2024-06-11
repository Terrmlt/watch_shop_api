from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField

from products.models import Product, Brand
from .brand_serializer import BrandSerializer


class ProductSerializer(serializers.ModelSerializer):
    brand = BrandSerializer(read_only=True)

    class Meta:
        model = Product
        fields = '__all__'


class CreateOrUpdateProductSerializer(serializers.ModelSerializer):
    brand = PrimaryKeyRelatedField(queryset=Brand.objects.all())

    class Meta:
        model = Product
        fields = '__all__'

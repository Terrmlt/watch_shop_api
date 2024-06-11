from rest_framework import serializers

from orders.models import Order
from orders.serializers import OrderItemSerializer


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ('id', 'address', 'created_at', 'items')

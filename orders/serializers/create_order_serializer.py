from django.contrib.auth import get_user_model
from rest_framework import serializers

from orders.models import Order, OrderItem
from .order_item_serializer import CreateOrderItemSerializer

UserModel = get_user_model()


class CreateOrderSerializer(serializers.ModelSerializer):
    items = CreateOrderItemSerializer(many=True)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Order
        fields = ('id', 'address', 'items', 'user',)
        extra_kwargs = {
            'id': {'read_only': True},
        }

    def create(self, validated_data):
        order = Order.objects.create(user=validated_data['user'], address=validated_data['address'])

        for item in validated_data['items']:
            order_item = OrderItem.objects.create(order=order, product=item['product'], quantity=item['quantity'])
            order_item.save()

        order.save()
        return order

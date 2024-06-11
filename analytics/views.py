from django.db.models import Sum, F
from drf_spectacular.utils import extend_schema
from rest_framework import status as statuses
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from common.permissions import IsManager
from orders.models import Order, OrderItem


@extend_schema(
    tags=['Analytic API'],
    responses={
        200: {'type': 'object', 'properties': {
            'total_orders': {'type': 'integer'},
            'total_revenue': {'type': 'integer'},
            'total_product_sold': {'type': 'integer'},
        }},
    }
)
@api_view(['GET'])
@permission_classes([IsAuthenticated & IsManager])
def summary(request):
    total_orders = Order.objects.all().count()
    total_revenue = OrderItem.objects.aggregate(total=Sum(F('quantity') * F('product__price')))['total']
    total_product_sold = OrderItem.objects.filter(
        order__status=Order.Status.DELIVERED
    ).aggregate(total_quantity=Sum('quantity'))['total_quantity'] or 0

    return Response({
        'total_orders': total_orders,
        'total_revenue': total_revenue,
        'total_product_sold': total_product_sold
    }, status=statuses.HTTP_200_OK)


@extend_schema(
    tags=['Analytic API'],
    responses={
        200: {'type': 'object', 'properties': {
            'pending_orders': {'type': 'integer'},
            'shipped_orders': {'type': 'integer'},
            'delivered_orders': {'type': 'integer'},
        }},
    }
)
@api_view(['GET'])
@permission_classes([IsAuthenticated & IsManager])
def status(request):
    pending_orders = Order.objects.filter(status=Order.Status.PENDING).count()
    shipped_orders = Order.objects.filter(status=Order.Status.SHIPPED).count()
    delivered_orders = Order.objects.filter(status=Order.Status.DELIVERED).count()

    return Response({
        'pending_orders': pending_orders,
        'shipped_orders': shipped_orders,
        'delivered_orders': delivered_orders
    }, status=statuses.HTTP_200_OK)

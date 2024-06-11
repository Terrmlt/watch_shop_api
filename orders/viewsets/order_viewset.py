from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from common.permissions import IsManager, IsOrderOwner
from orders.models import Order
from orders.serializers import OrderSerializer, CreateOrderSerializer


@extend_schema(tags=['Order API'])
class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    @extend_schema(parameters=[
        OpenApiParameter(name='client_id',
                         required=True,
                         type=OpenApiTypes.STR,
                         location=OpenApiParameter.QUERY,
                         description='Client ID'),
    ])
    @action(detail=False, methods=['GET'])
    def my(self, request):
        client_id = request.query_params.get('client_id', None)

        if not client_id:
            return Response('Query param client_id is required', status=status.HTTP_400_BAD_REQUEST)

        orders = self.get_queryset().filter(user_id=client_id).order_by('created_at')
        page = self.paginate_queryset(orders)
        serialize = self.get_serializer(page, many=True)
        return self.get_paginated_response(serialize.data)

    @extend_schema(request=CreateOrderSerializer)
    def create(self, request, *args, **kwargs):
        serializer = CreateOrderSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_permissions(self):
        actions_permissions = {
            'create': [IsAuthenticated],
            'my': [IsAuthenticated & (IsManager | IsOrderOwner)],
            'retrieve': [IsAuthenticated & (IsManager | IsOrderOwner)],
        }

        if self.action in actions_permissions.keys():
            permission_classes = actions_permissions[self.action]
        else:
            permission_classes = [IsAuthenticated & IsManager]

        return [permission() for permission in permission_classes]

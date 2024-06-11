from rest_framework.permissions import BasePermission

from orders.models import Order


class IsOrderOwner(BasePermission):
    def has_permission(self, request, view):

        if view.action == 'my':
            client_id = request.query_params.get('client_id', None)
            return client_id is not None and str(request.user.id) == client_id

        if view.action == 'retrieve':
            order = Order.objects.filter(user=request.user, id=view.kwargs['pk']).first()
            return order is not None

        return False

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user

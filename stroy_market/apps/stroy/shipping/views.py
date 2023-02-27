from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from apps.stroy.shipping.models import Order, OrderItem, OrderAddress
from apps.stroy.shipping.serializers import OrderSerializer, OrderCreateSerializer, OrderItemSerializer, OrderAddressSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAdminUser]

    @action(detail=True, methods=['get'])
    def get_order_items(self, request):
        order = self.get_object()
        queryset = order.orderitem_set.all()
        serializer = OrderItemSerializer(queryset, many=True)
        pagination = self.paginate_queryset(queryset)
        if pagination is not None:
            return self.get_paginated_response(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get_permissions(self):
        if self.action in ['create', 'get_order_items', 'get_order_address', 'retrieve']:
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.action == 'create':
            return OrderCreateSerializer
        return OrderSerializer
    

class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [permissions.IsAdminUser]

    def get_permissions(self):
        if self.action in ['retrieve', 'create']:
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in permission_classes]


class OrderAddressViewSet(viewsets.ModelViewSet):
    queryset = OrderAddress.objects.all()
    serializer_class = OrderAddressSerializer
    permission_classes = [permissions.IsAdminUser]
    lookup_field = 'id'

    def get_permissions(self):
        if self.action in ['create', 'retrieve']:
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in permission_classes]
    
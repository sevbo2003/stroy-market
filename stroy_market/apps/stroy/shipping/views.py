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
    http_method_names = ['get', 'post', 'head', 'options']

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
        return [permission() for permission in permission_classes]
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        session_key = request.session.session_key
        if request.user.is_authenticated:
            if instance.user != request.user:
                return Response(status=status.HTTP_403_FORBIDDEN)
        else:
            if instance.session_key != session_key:
                return Response(status=status.HTTP_403_FORBIDDEN)
        serializer = self.get_serializer(instance)
        order_data = serializer.data
        return Response(
            order_data,
            status=status.HTTP_200_OK
        )

    def get_serializer_class(self):
        if self.action == 'create':
            return OrderCreateSerializer
        return OrderSerializer
    

class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [permissions.IsAdminUser]
    http_method_names = ['get', 'post', 'head', 'options']

    def get_permissions(self):
        if self.action in ['retrieve', 'create']:
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in permission_classes]
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        session_key = request.session.session_key
        if request.user.is_authenticated:
            if instance.order.user != request.user:
                return Response(status=status.HTTP_403_FORBIDDEN)
        else:
            if instance.order.session_key != session_key:
                return Response(status=status.HTTP_403_FORBIDDEN)
        serializer = self.get_serializer(instance)
        order_item_data = serializer.data
        return Response(
            order_item_data,
            status=status.HTTP_200_OK
        )

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_authenticated:
            queryset = queryset.filter(order__user=self.request.user)
        else:
            queryset = queryset.filter(order__session_key=self.request.session.session_key)
        return queryset


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
    
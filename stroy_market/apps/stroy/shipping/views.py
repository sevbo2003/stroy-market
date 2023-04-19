from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from apps.stroy.shipping.models import Order, OrderItem, OrderAddress, PromoCode
from apps.stroy.shipping.serializers import (
    OrderSerializer,
    OrderCreateSerializer,
    OrderItemSerializer,
    OrderAddressSerializer,
    CheckPromocodeSerializer,
)


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    http_method_names = ["get", "post", "head", "options"]

    @action(detail=True, methods=["get"])
    def get_order_items(self, request):
        order = self.get_object()
        queryset = order.orderitem_set.all()
        serializer = OrderItemSerializer(queryset, many=True)
        pagination = self.paginate_queryset(queryset)
        if pagination is not None:
            return self.get_paginated_response(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get_queryset(self):
        if self.request.user.is_staff:
            return Order.objects.all()
        else:
            if self.request.user.is_authenticated:
                return Order.objects.filter(user=self.request.user)
            return Order.objects.filter(session_key=self.request.session.session_key)

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
        return Response(order_data, status=status.HTTP_200_OK)

    def get_serializer_class(self):
        if self.action == "create":
            return OrderCreateSerializer
        return OrderSerializer


class OrderAddressViewSet(viewsets.ModelViewSet):
    queryset = OrderAddress.objects.all()
    serializer_class = OrderAddressSerializer
    lookup_field = "id"

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_authenticated:
            queryset = queryset.filter(order__user=self.request.user)
        else:
            queryset = queryset.filter(
                order__session_key=self.request.session.session_key
            )
        return queryset

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
        order_address_data = serializer.data
        return Response(order_address_data, status=status.HTTP_200_OK)


class CheckPromocodeViewSet(viewsets.ModelViewSet):
    queryset = PromoCode.objects.all()
    serializer_class = CheckPromocodeSerializer
    http_method_names = ["get", "head", "options"]
    lookup_field = "code"

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.active:
            return Response(
                data={"message": f"Promocode mavjud", "discount": instance.discount},
                status=status.HTTP_200_OK,
            )
        return Response(status=status.HTTP_404_NOT_FOUND)

    def list(self, request, *args, **kwargs):
        return Response(data={"message": "Not found"}, status=status.HTTP_404_NOT_FOUND)

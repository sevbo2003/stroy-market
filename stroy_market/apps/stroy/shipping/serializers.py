from rest_framework import serializers
from apps.stroy.shipping.models import Order, OrderItem, OrderAddress
from django.contrib.auth import get_user_model


User = get_user_model()


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ('id', 'order', 'product', 'quantity','product_color','product_size', 'price')


class OrderAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderAddress
        fields = ['id', 'delivery', 'payment', 'name', 'phone', 'lat', 'lon', 'address', 'comment', 'date']


class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True)
    order_address = OrderAddressSerializer(many=True)

    class Meta:
        model = Order
        fields = ('id', 'user', 'status', 'created_at', 'updated_at', 'order_items', 'order_address', 'get_total_price', 'get_total_weight')


class OrderCreateSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False)
    status = serializers.CharField(required=False)

    class Meta:
        model = Order
        fields = ('id', 'user', 'status', 'created_at', 'updated_at')
    
    def update(self, instance, validated_data):
        instance.status = validated_data.get('status', instance.status)
        instance.save()
        return instance
    
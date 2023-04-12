from rest_framework import serializers
from apps.stroy.shipping.models import Order, OrderItem, OrderAddress
from apps.stroy.models import PromoCode
from django.contrib.auth import get_user_model
from apps.stroy.models import CartItem


User = get_user_model()


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ('id', 'order', 'product', 'quantity', 'price')


class OrderAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderAddress
        fields = ['id','order', 'delivery', 'payment', 'name', 'phone', 'lat', 'lon', 'address', 'comment', 'date']


class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True)
    order_address = OrderAddressSerializer(many=True)

    class Meta:
        model = Order
        fields = ('id', 'user', 'status', 'created_at', 'updated_at', 'order_items', 'order_address', 'get_total_price', 'get_total_weight')


class OrderCreateSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(required=False, read_only=True)
    status = serializers.CharField(required=False, default='pending', read_only=True)
    promocode = serializers.CharField(required=False)

    class Meta:
        model = Order
        fields = ('id', 'user', 'status', 'promocode', 'created_at', 'updated_at')
    

    def validate_promocode(self, value):
        if value:
            if not PromoCode.objects.filter(code=value).exists():
                raise serializers.ValidationError('Promocode topilmadi')
            if not PromoCode.objects.filter(code=value).first().active:
                raise serializers.ValidationError('Promocodeni aktivlashtirish muddati tugagan')
        return value
    
    def create(self, validated_data):
        request = self.context.get('request')
        if request.user.is_authenticated:
            validated_data['user'] = request.user
            data = super().create(validated_data)
            cart_items = CartItem.objects.filter(user=request.user)
            OrderItem.objects.bulk_create([
                OrderItem(order=data, product=item.product, quantity=item.quantity, price=item.product.price) for item in cart_items
            ])
            return data
        else:
            session_key = request.session.session_key
            if not session_key:
                request.session.save()
                session_key = request.session.session_key
            validated_data['session_key'] = session_key
            data =  super().create(validated_data)
            cart_items = CartItem.objects.filter(session_key=session_key)
            OrderItem.objects.bulk_create([
                OrderItem(order=data, product=item.product, quantity=item.quantity, price=item.product.price) for item in cart_items
            ])
            return data
 
    
from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from apps.stroy.models import Product
import uuid
from apps.stroy.models import PromoCode
from django.db.models import Sum, F, FloatField, ExpressionWrapper

User = get_user_model()


class Order(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    STATUS_CHOICES = (
        ('pending', _('Pending')),
        ('processing', _('Processing')),
        ('shipped', _('Shipped')),
        ('delivered', _('Delivered')),
        ('cancelled', _('Cancelled')),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    session_key = models.CharField(max_length=100, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    promocode = models.ForeignKey(PromoCode, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Buyurtma')
        verbose_name_plural = _('Buyurtmalar')
        ordering = ('-updated_at',)

    def __str__(self):
        return f'Buyurtma {self.pk}'

    @property
    def get_total_price(self):
        if self.orderitem_set.exists():
            if self.order_address.exists():
                if self.order_address.first().delivery == 'free':
                    price = self.orderitem_set.first().total_price(self)
                    if self.promocode:
                        return price - (price * self.promocode.discount / 100)
                    return price
                else:
                    price = self.orderitem_set.first().total_price(self) + int(settings.DELIVERY_COST)
                    if self.promocode:
                        return price - (price * self.promocode.discount / 100)
            price = self.orderitem_set.first().total_price(self)
            if self.promocode:
                return price - (price * self.promocode.discount / 100)
            return price
        return None
    
    @property
    def get_total_weight(self):
        return OrderItem.total_weight(self)
    
    @property
    def order_items(self):
        return OrderItem.get_order_items(self)
    
    @property
    def order_address(self):
        return OrderAddress.objects.filter(order=self).first()

    @classmethod
    def get_order_items(cls, order):
        return OrderItem.get_order_items(order)
    
    @classmethod
    def get_order_address(cls, order):
        return OrderAddress.objects.filter(order=order).first()
    
    @classmethod
    def total_weight(cls, order):
        return OrderItem.total_weight(order)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    class Meta:
        verbose_name = _('Order item')
        verbose_name_plural = _('Order items')

    def __str__(self):
        return f'{self.quantity} x {self.product.name}'
    
    def save(self, *args, **kwargs):
        self.price = self.product.price_with_discount * self.quantity
        super().save(*args, **kwargs)
    
    @classmethod
    def get_order_items(cls, order):
        return cls.objects.filter(order=order)
    
    @classmethod
    def total_price(cls, order):
        return sum(item.product.price_with_discount * item.quantity for item in cls.get_order_items(order))
    
    @classmethod
    def total_weight(cls, order):
        return sum(item.product.weight * item.quantity for item in cls.get_order_items(order))


class OrderAddress(models.Model):
    DELIVERY_CHOICES = (
        ('free', _('Free')),
        ('paid', _('Paid')),
    )
    PAYMENT_CHOICES = (
        ('cash', _('Cash')),
        ('card', _('Card')),
    )
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order_address", blank=True, null=True)
    delivery = models.CharField(max_length=20, choices=DELIVERY_CHOICES, default='free')
    payment = models.CharField(max_length=20, choices=PAYMENT_CHOICES, default='cash')
    name = models.CharField(max_length=125)
    phone = models.CharField(max_length=125)
    lat = models.DecimalField(max_digits=10, decimal_places=6, blank=True, null=True)
    lon = models.DecimalField(max_digits=10, decimal_places=6, blank=True, null=True)
    address = models.CharField(max_length=125)
    comment = models.CharField(max_length=125, null=True, blank=True)
    date = models.DateField(auto_now_add=True)
    shipping_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = _('Buyurma manzili')
        verbose_name_plural = _('Buyurma manzillari')
        ordering = ('-date',)

    def __str__(self):
        return self.name

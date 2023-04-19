from django.contrib import admin
from apps.stroy.shipping.models import Order, OrderItem, OrderAddress


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


class OrderAddressInline(admin.TabularInline):
    model = OrderAddress
    extra = 0


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status', 'promocode', 'created_at', 'updated_at', 'get_total_weight', )
    list_filter = ('status',)
    inlines = [OrderItemInline, OrderAddressInline]


admin.site.register(Order, OrderAdmin)

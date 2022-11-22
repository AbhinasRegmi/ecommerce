from django.contrib import admin

from .models import Order, OrderItem


@admin.register(Order)
class OrderAdminConfig(admin.ModelAdmin):
    list_display = ['email', 'intent', 'total_amount', 'updated_at', 'billing_status']

@admin.register(OrderItem)
class OrderItemAdminConfig(admin.ModelAdmin):
    list_display = ['product', 'order', 'quantity']

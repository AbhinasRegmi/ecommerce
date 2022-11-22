# from decimal import Decimal
from django.db import models
from django.conf import settings
# from django_countries.fields import CountryField


from store.models import Product

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    total_amount = models.DecimalField(max_digits=5, decimal_places=2)
    intent = models.CharField(max_length=255)
    secret = models.CharField(max_length=255)
    billing_status = models.BooleanField(default=False)


    class Meta:
        ordering = ['-created_at']


    def __str__(self):
        return f"{self.intent}"

    def email(self):
        return self.user.email



class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    unit_price = models.DecimalField(max_digits=5, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)

    def total_amount(self):
        return self.unit_price * self.quantity
from django.db import models
from django.conf import settings

from django.urls import reverse

# Create your models here.
class Category(models.Model):

    #db_index=True helps in search optimization with space tradeoff
    name = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(max_length=255, unique=True)

    def __str__(self):
        return self.name

    def total_items(self):
        return self.product_set.all().count()

    def get_absolute_url(self):
        return reverse('store:category-view', kwargs={'slug': self.slug})

    class Meta:
        #in admin panel it will say categories instead of categorys
        verbose_name_plural='categories'


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    author = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to='product/images/')

    in_stock = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']

    
    def get_absolute_url(self):
        return reverse('store:product-view', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title
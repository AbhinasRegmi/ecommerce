from django.contrib import admin
from .models import Category, Product


@admin.register(Category)
class CategoryAdminConfig(admin.ModelAdmin):
    prepopulated_fields = {'slug': ['name']}

@admin.register(Product)
class ProductAdminConfig(admin.ModelAdmin):
    prepopulated_fields = {'slug': ['title']}
    list_display = ['title', 'category', 'in_stock', 'price']
    list_filter = ['in_stock']
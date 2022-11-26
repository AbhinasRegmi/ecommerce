from django.contrib import admin

from mptt.admin import ModelAdmin

from .models import (
    Category,
    ProductType,
    ProductSpecification,
    ProductSpecificationValue,
    Product,
    ProductImage
)


# @admin.register(Category)
# class CategoryAdminConfig(admin.ModelAdmin):
#     list_display = ['name', 'total_items']
#     prepopulated_fields = {'slug': ['name']}

# @admin.register(Product)
# class ProductAdminConfig(admin.ModelAdmin):
#     prepopulated_fields = {'slug': ['title']}
#     list_display = ['title', 'category', 'in_stock', 'price']
#     list_filter = ['in_stock']
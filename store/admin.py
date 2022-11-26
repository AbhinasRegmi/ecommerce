from django import forms
from django.contrib import admin

from mptt.admin import MPTTModelAdmin

from .models import (
    Category,
    ProductType,
    ProductSpecification,
    ProductSpecificationValue,
    Product,
    ProductImage
)


@admin.register(Category)
class CategoryAdminConfig(MPTTModelAdmin):
    prepopulated_fields = {'slug': ['name']}

class ProductSpecificationInline(admin.TabularInline):
    model=ProductSpecification

@admin.register(ProductType)
class ProductTypeAdmin(admin.ModelAdmin):
    inlines = [ 
        ProductSpecificationInline
    ]


class ProductImageInline(admin.TabularInline):
    model = ProductImage

class ProductSpecificationValueInline(admin.TabularInline):
    model = ProductSpecificationValue


@admin.register(Product)
class ProductAdminConfig(admin.ModelAdmin):
    inlines = [ 
        ProductSpecificationValueInline,
        ProductImageInline
    ]

    prepopulated_fields = {'slug': ['title']}
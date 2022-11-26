from django.db import models
from django.urls import reverse

from mptt.models import TreeForeignKey, MPTTModel

from .validators import validate_max_image_size


class Category(MPTTModel):
    """Category is implemented with mptt so we can have dynamic relations between
        categories like tree
    """
    name = models.CharField(
        max_length=255,
        unique=True,
        db_index=True,

        verbose_name='Category Name',
        help_text='The category name must be unique.',
    )

    slug = models.SlugField(
        max_length=255,
        unique=True,
        db_index=True,
    )

    #the nodes on tree will have parents, we will set parent to self
    #so that we can build category tree
    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children',
    )

    is_active = models.BooleanField(default=True)

    #documentation says we need this
    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        verbose_name_plural='Categories'

    def __str__(self):
        return self.name


    def get_absolute_url(self):
        return reverse(
            'store:category-view',
            kwargs={'slug': self.slug},
        )


class ProductType(models.Model):
    name = models.CharField(
        max_length=255,
        unique=True,
    )

    is_active = models.BooleanField(
        default=True
    )

    class Meta:
        verbose_name = ['Product Type']
        verbose_name_plural = ['Product Types']

    def __str__(self):
        return self.name

class ProductSpecification(models.Model):
    """
    This contains the feature of product it is associated with. Like isbn, pages, etc.
    And it is liked with product type so all product type will have its own features.
    """

    name = models.CharField(
        max_length=255,
    )

    product_type = models.ForeignKey(
        'ProductType',
        on_delete=models.RESTRICT,
    )

    class Meta:
        verbose_name = ['Product Specification']
        verbose_name_plural = ['Product Specifications']

    def __str__(self):
        return self.name


class Product(models.Model):
    """
        This model is the actual product that has categories, product types, images
    """

    product_type = models.ForeignKey(
        ProductType,
        on_delete=models.RESTRICT,
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.RESTRICT,
    )


    title = models.CharField(
        max_length=255,
    )
    description = models.TextField(
        blank=True,   
    )
    slug = models.SlugField(
        max_length=255,
    )

    price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        help_text='Price in Nepalese Rupees.',
    )


    is_active = models.BooleanField(
        default=True,
    )
    in_stock = models.BooleanField(
        default=True,
    )


    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
    )


    class Meta:
        ordering = ['updated_at']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('store:product-view', kwargs={'slug': self.slug})



class ProductSpecificationValue(models.Model):
    """
        This model is for some product with specific features. Like a book with lucky draw inside.
    """

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
    )
    specification = models.ForeignKey(
        ProductSpecification,
        on_delete=models.RESTRICT,
    )


    value = models.CharField(
        max_length=255,
        help_text='The product specific value in less than 255 words.'
    )

    class Meta:
        verbose_name = ['Product Specification Value']
        verbose_name_plural = ['Product Specification Values']

    def __str__(self):
        return self.value



class ProductImage(models.Model):
    """
        A single product may have multiple images, so we store multiple images with a featured image here.
    """

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
    )

    image = models.ImageField(
        upload_to=f'product/{product}/',
        default='product/default.png',
        validators=[validate_max_image_size],
    )

    is_featured = models.BooleanField(
        default=False,
    )

    class Meta:
        verbose_name = ['Product Image']
        verbose_name_plural = ['Product Images']

    



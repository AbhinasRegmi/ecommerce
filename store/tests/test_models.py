from django.test import TestCase
from django.contrib.auth.models import User
from store.models import Category, Product


class TestCategoryModel(TestCase):

    def setUp(self):
        self.data1 = Category.objects.create(name='test', slug='test')
        self.count = self.data1.product_set.all().count()
    
    def test_str_method(self):
        self.assertEqual(str(self.data1), 'test')

    def test_category_model_entry(self):
        data = self.data1
        self.assertTrue(isinstance(data, Category))
    
    def test_category_count(self):
        data = self.data1
        self.assertEqual(data.total_items(), self.count)


class TestProductModel(TestCase):

    def setUp(self):
        Category.objects.create(name='test', slug='test')
        User.objects.create(username='admin')

        self.data = Product.objects.create(category_id=1, created_by_id=1, title='product', slug='product', author='test', price=10, image='test')

    def test_str(self):
        self.assertEqual(str(self.data), 'product')
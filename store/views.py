from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from .models import Category, Product, ProductImage


#access this from setting templates context to send this to all pages

class HomeView(ListView):
    context_object_name = 'product_list'
    paginate_by = 10
    template_name = 'store/home-view.html'
    queryset = Product.objects.all().order_by('-updated_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['images'] = ProductImage.objects.all()
        return context


class ProductView(DetailView):
    context_object_name = 'product'
    template_name = 'store/product-view.html'

    def get_queryset(self):
        return Product.objects.filter(slug=self.kwargs.get('slug'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_tree'] = Category.objects.filter(product__slug=self.kwargs.get('slug')).get_ancestors(include_self=True)
        return context

class CategoryView(ListView):
    context_object_name = 'product_list'
    template_name = 'store/category-view.html'

    def get_queryset(self):
        #we need to return children under the category name too.
        if self.kwargs.get('slug') == 'all':
            categories = Category.objects.filter().get_descendants(include_self=True)
        else:
            categories = Category.objects.filter(slug=self.kwargs.get('slug')).get_descendants(include_self=True)
        return Product.objects.filter(category__name__in=[str(name) for name in categories])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_tree'] = Category.objects.filter(slug=self.kwargs.get('slug')).get_ancestors(include_self=True)
        return context
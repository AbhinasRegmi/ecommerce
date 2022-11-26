from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from .models import Category, Product


#access this from setting templates context to send this to all pages

class HomeView(ListView):
    context_object_name = 'product_list'
    paginate_by = 10
    template_name = 'store/home-view.html'
    queryset = Product.objects.all().order_by('-updated_at')


class ProductView(DetailView):
    context_object_name = 'product'
    template_name = 'store/product-view.html'

    def get_queryset(self):
        return Product.objects.filter(slug=self.kwargs.get('slug'))

class CategoryView(ListView):
    context_object_name = 'product_list'
    template_name = 'store/category-view.html'

    def get_queryset(self):
        #we need to return children under the category name too.
        self.category = ''
        return Product.objects.filter(category=self.category)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context
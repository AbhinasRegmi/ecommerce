from django.views.generic.detail import DetailView
from django.views.generic.base import TemplateView

class BasketSumView(TemplateView):
    template_name = 'basket/basket-sum-view.html'
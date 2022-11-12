from django.views.generic.base import TemplateView
from django.views import View
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from store.models import Product
from .basket import BasketSessions
import json

class BasketSumView(TemplateView):
    template_name = 'basket/basket-sum-view.html'

class BasketAddView(View):
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        product_id = int(data.get('product_id'))
        product_count = int(data.get('product_count'))

        basket = BasketSessions(request)
        basket.addSessionData(
            product=get_object_or_404(Product, pk=product_id),
            count=product_count
        )

        return JsonResponse({'count': 100})


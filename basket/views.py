from django.views.generic.base import TemplateView
from django.http import HttpResponse
import json

class BasketSumView(TemplateView):
    template_name = 'basket/basket-sum-view.html'


def basket_add(request):
    if request.method == "POST":
        data = json.loads(request.body)
        return HttpResponse(content={'data': data})
    else:
        return HttpResponse('get request not allowed here.')

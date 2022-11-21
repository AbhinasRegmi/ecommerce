from django.http import JsonResponse
from django.views.generic import View
import json


from .models import Order, OrderItem
from basket.basket import BasketSessions


class OrderAddView(View):
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):

        post_data = json.loads(self.request.body)
        session = BasketSessions(self.request)

        user = self.request.user.id
        order_key = post_data.get('order_key')
        total_price = session.getTotalPrice()


        data = {
            'message': 'The post was successfull.'
        }

        return JsonResponse(data)

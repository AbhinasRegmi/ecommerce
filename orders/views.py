import json
from django.http import JsonResponse
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Order, OrderItem
from payments.views import createPaymentIntent as create_intent
from basket.basket import BasketSessions


def add_orders(request, intent):
    session = BasketSessions(request)
    order_key = intent
    total_price = session.getTotalPrice()

    data = {}

    if not Order.objects.filter(order_key=order_key).exists():
            # create a new order.
            order = Order.objects.create(
                user=request.user,
                total_amount=total_price,
                order_key=order_key
            )

            #add all the products in basket to orderItem
            for item in session:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    unit_price=item['price'],
                    quantity=item['count']
                )
            
            #also delete the products from the session
            session.deleteAllSession(request=request)

            data = {
            'success' : 'ok',
            'message': 'Check you dashboard for orders placed.'
            }

    return data


class OrderAddView(LoginRequiredMixin, View):
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        data = add_orders(request=self.request, intent=json.loads(self.request.body).get('order_key'))
        return JsonResponse(data)


class OrderSaveView(LoginRequiredMixin, View):
    http_method_names = ['get']

    def get(self, request, *args, **kwargs):
        _, intent = create_intent(request=self.request)
        data = add_orders(request=self.request, intent=intent)
        return JsonResponse(data)
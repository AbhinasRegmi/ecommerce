import json
from django.http import JsonResponse
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Order, OrderItem
from payments.views import createPaymentIntent as create_intent
from basket.basket import BasketSessions


def add_orders(request, intent, secret):
    session = BasketSessions(request)
    total_price = session.getTotalPrice()

    data = {}

    if not Order.objects.filter(intent=intent, secret=secret).exists():
            # create a new order.
            order = Order.objects.create(
                user=request.user,
                total_amount=total_price,
                intent=intent,
                secret=secret
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
        body = json.loads(self.request.body)
        data = add_orders(request=self.request, intent=body.get('intent'), secret=body.get('secret'))
        return JsonResponse(data)


class OrderSaveView(LoginRequiredMixin, View):
    http_method_names = ['get']

    def get(self, request, *args, **kwargs):
        secret, intent = create_intent(request=self.request)
        data = add_orders(request=self.request, intent=intent, secret=secret)
        return JsonResponse(data)
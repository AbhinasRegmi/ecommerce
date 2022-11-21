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

        order_key = post_data.get('order_key')
        total_price = session.getTotalPrice()

        data = {}

        if not Order.objects.filter(order_key=order_key).exists():
            # create a new order.
            order = Order.objects.create(
                user=self.request.user,
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
            session.deleteAllSession(request=self.request)

            data = {
            'success' : 'ok',
            'message': 'Check you dashboard for orders placed.'
        }

        return JsonResponse(data)

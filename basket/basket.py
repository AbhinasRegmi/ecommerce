
class BasketSessions():

    def __init__(self, request):
        self.session = request.session
        basket = self.session.get('basket_skey')

        if not basket:
            basket = self.session['basket_skey'] = {}

        self.basket = basket

        # del request.session['basket_skey']

    def addSessionData(self, product, count):

        if not str(product.id) in self.basket:
            self.basket[str(product.id)] = {
                'count': count,
                'price': str(product.price),
                'total_price': str(count * product.price)
            }
        else:
            self.basket[str(product.id)]['count'] += count
            self.basket[str(product.id)]['price'] = str(product.price)
            self.basket[str(product.id)]['total_price'] = str(product.price * self.basket[str(product.id)]['count'])

        self.session.modified = True
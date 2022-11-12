
class BasketSessions():

    def __init__(self, request):
        self.session = request.session
        basket = self.session.get('basket_skey')

        if 'basket_skey' not in self.session:
            basket = self.session['basket_skey'] = {'test': 2}

        self.basket = basket

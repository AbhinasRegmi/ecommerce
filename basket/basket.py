
class BasketSessions():

    def __init__(self, request):
        self.session = request.session
        basket = self.session.get('basket_skey')

        if not basket:
            basket = self.session['basket_skey'] = {}

        self.basket = basket
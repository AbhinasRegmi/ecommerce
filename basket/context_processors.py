from .basket import BasketSessions

def basket(request):
    basket = BasketSessions(request)

    return {
        'basket': basket,
    }


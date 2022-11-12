from .basket import BasketSessions

def basket(request):
    return {
        'basket': BasketSessions(request)
    }
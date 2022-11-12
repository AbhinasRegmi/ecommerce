from .basket import BasketSessions

def basket(request):
    basket = BasketSessions(request)
    count = basket.countTotalProduct()

    return {
        'basket': basket,
        'product_count': count
    }


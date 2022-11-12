from store.models import Product
from decimal import Decimal

class BasketSessions():

    def __init__(self, request):
        self.session = request.session
        basket = self.session.get('basket_skey')

        if not basket:
            basket = self.session['basket_skey'] = {}

        self.basket = basket

        # del request.session['basket_skey']

    def __len__(self):
        # counting total products
        total_count = 0
        for product in self.basket.values():
            total_count += int(product['count'])

        return total_count

    
    def __iter__(self):
        """
            make this object iteralble and return products
        """
        product_ids = [ int(i) for i in self.basket.keys() ]
        products = Product.objects.filter(is_active=True, id__in=product_ids)
        cpy_basket = self.basket.copy()

        for product in products:
            cpy_basket[str(product.id)]['product'] = product
        
        for item in cpy_basket.values():
            yield item

    def getTotalPrice(self):
        total = 0
        for product in self.basket.values():
            total += Decimal(product['total_price'])

        return total


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

        return len(self)


    def updateSessionData(self, product, count):
        
        self.basket[str(product.id)]['count'] = count
        self.basket[str(product.id)]['price'] = str(product.price)
        self.basket[str(product.id)]['total_price'] = str(product.price * self.basket[str(product.id)]['count'])

        self.session.modified = True

        return {
            'count': len(self),
            'total_price': self.getTotalPrice(),
            'sub_price': self.basket[str(product.id)]['total_price']
        }

    def deleteSessionData(self, product_id):

        if str(product_id) in self.basket:
            del self.basket[str(product_id)]
            self.session.modified = True
            
            return {
                'count': len(self),
                'total_price': self.getTotalPrice()
            }
        else:
            return None

        
        

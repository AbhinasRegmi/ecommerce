from django.urls import path

from .views import BasketSumView

app_name = 'basket'
urlpatterns = [
    path('', BasketSumView.as_view(), name='basket-sum-view')  
]
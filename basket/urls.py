from django.urls import path

from .views import BasketSumView, basket_add

app_name = 'basket'
urlpatterns = [
    path('', BasketSumView.as_view(), name='basket-sum-view'),
    path('add/',basket_add, name='basket-add'),
]
from django.urls import path

from .views import BasketSumView, BasketAddView, BasketDeleteView, BasketUpdateView

app_name = 'basket'
urlpatterns = [
    path('', BasketSumView.as_view(), name='basket-sum-view'),
    path('add/', BasketAddView.as_view(), name='basket-add'),
    path('delete/', BasketDeleteView.as_view(), name='basket-delete'),
    path('update/', BasketUpdateView.as_view(), name='basket-update'),
]
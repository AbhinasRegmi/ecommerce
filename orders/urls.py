from django.urls import path


from .views import OrderAddView, OrderSaveView

app_name = 'orders'
urlpatterns = [  
    path('add/', OrderAddView.as_view(), name='add'),
    path('save/', OrderSaveView.as_view(), name='save'),
]
from django.urls import path


from .views import PaymentIntentView, CheckoutView

app_name='payments'
urlpatterns = [  
    path('intent/', PaymentIntentView.as_view(), name='intent'),
    path('', CheckoutView.as_view(), name='checkout'),
]
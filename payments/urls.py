from django.urls import path


from .views import PaymentIntentView, CheckoutView, PaymentConfirmationWebhook

app_name='payments'
urlpatterns = [  
    path('intent/', PaymentIntentView.as_view(), name='intent'),
    path('webhook/', PaymentConfirmationWebhook.as_view(), name='webhook'),
    path('', CheckoutView.as_view(), name='checkout'),
]
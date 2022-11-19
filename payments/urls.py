from django.urls import path


from .views import CheckoutView

app_name='payments'

urlpatterns = [  

    path('', CheckoutView.as_view(), name='checkout'),
]
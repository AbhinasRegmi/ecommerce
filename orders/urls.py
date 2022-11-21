from django.urls import path


from .views import OrderAddView

app_name = 'orders'
urlpatterns = [  
    
    path('add/', OrderAddView.as_view(), name='add'),
]
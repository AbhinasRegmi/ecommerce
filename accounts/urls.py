from django.urls import path

from .views import RegistrationView, LoginView, DashboardView, activate_view

app_name = 'accounts'
urlpatterns = [  
    
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('login/', LoginView.as_view(), name='login'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('activate/<str:uid>/<str:token>', activate_view, name='activate'),
]
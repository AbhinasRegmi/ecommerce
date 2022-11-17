from django.urls import path

from .views import RegistrationView, LoginView, DashboardView, activate_view, LogoutView, UpdateProfileView, ResetYourPasswordView, ResetPasswordDoneView

app_name = 'accounts'
urlpatterns = [  
    
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('dashboard/edit/', UpdateProfileView.as_view(), name='updateprofile' ),
    path('activate/<str:uidb64>/<str:token>', activate_view, name='activate'),
    path('reset/', ResetYourPasswordView.as_view(), name='passwordreset'),
    #using specific name uidb64 because we will be using builtin view
    path('reset/confirm/<str:uidb64>/<str:token>/', ResetPasswordDoneView.as_view(), name='passwordresetdone'),
]
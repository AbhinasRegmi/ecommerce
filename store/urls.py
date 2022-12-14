from django.urls import path

from .views import HomeView, ProductView, CategoryView

#this name should match with that in core's urls namespace
app_name = 'store'
urlpatterns = [  
    path('', HomeView.as_view(), name='home-view'),
    path('<slug:slug>', ProductView.as_view(), name='product-view'),
    path('shop/<slug:slug>', CategoryView.as_view(), name='category-view'),
]
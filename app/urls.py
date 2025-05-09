from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home_view, name='home'),
    path('about/', views.Aboutus_view, name='about'),
    path('service/', views.Service_view, name='service'),
    path('gallery/', views.Gallery_view, name='gallery'),
    path('contact/', views.ContactUs_view, name='contact'),
    path('get-available-times/', views.get_available_times, name='get_available_times'),
]

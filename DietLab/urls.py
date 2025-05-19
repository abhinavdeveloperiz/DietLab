from django.contrib import admin
from django.urls import path
from app import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.Home_view, name="home"),
    # path("appoinment/", views.Appoinment_view, name="appoinment"),
    path("payment/success/", views.payment_success_view, name="payment_success"),
    path("payment/cancel/", views.payment_cancel_view, name="payment_cancel"), 
    path("service/", views.Service_view, name="service"),
    path("about/", views.Aboutus_view, name="about"),
    path("contact/", views.ContactUs_view, name="contact"),
    path("gallery/", views.Gallery_view, name="gallery"),

    # path("payment-success/", views.payment_success, name="payment_success"),
    # path("payment-cancelled/", views.payment_cancelled, name="payment_cancelled"),
    
    
    # path("bookings/", views.My_Appointments_view, name="my_booking"),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

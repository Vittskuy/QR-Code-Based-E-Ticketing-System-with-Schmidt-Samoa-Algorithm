from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'), # url halaman home
    path('details/', views.details, name='details'), # url halaman detail
    path('confirmation/', views.confirmation, name='confirmation'), # url halaman konfirmasi
    path('thankyou/', views.thankyou, name='thankyou'), # url halaman thankyou
]

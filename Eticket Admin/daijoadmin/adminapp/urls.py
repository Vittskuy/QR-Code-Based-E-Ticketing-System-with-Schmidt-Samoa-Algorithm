from django.urls import path
from . import views

urlpatterns = [
    path('', views.admin_login, name='admin_login'), # UTL untuk halaman login (home)
    path('scan/', views.scan_qr_code, name='scan_qr_code'),  # URL untuk halaman scan QR code
    path('validate/', views.validate_ticket, name='validate_ticket'),  # URL untuk validasi tiket
    path('logout/', views.admin_logout, name='admin_logout'),  # URL untuk logout
]
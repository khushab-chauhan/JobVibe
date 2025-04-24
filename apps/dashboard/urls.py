from django.urls import path
from apps.dashboard.views import *

urlpatterns = [
    path('',login_page,name='login'),
    path('register/',register_page,name='register'),
    path('dashboard/',dashboard_page,name='dashboard'),
    path('forgot_password/',forgot_password_page,name='forgot_password'),
    path('otp_password/',otp_password_page,name='otp_password'),
    path('otp_register/',otp_register_page,name='otp_register'),
]
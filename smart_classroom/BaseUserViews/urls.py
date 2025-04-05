from django.urls import path
from utils.helpers.auths import refresh_token
from smart_classroom.BaseUserViews import (user_login, get_user_address, contact_request,
                                            get_csrf_token, verify_otp)

"""Base User API urls"""

urlpatterns = [
    path('login/', user_login.view, name='user_login'),
    path('refresh_token/', refresh_token, name='refresh_token'),
    path('address/', get_user_address.view, name='get_user_address'),
    path('contact/', contact_request.view, name='contact_request'),
    path('csrf/', get_csrf_token.view, name='get_csrf_token'),
    path('verify-otp/', verify_otp.view, name='verify_otp')
]
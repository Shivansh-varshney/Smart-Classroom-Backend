from django.urls import path
from utils.helpers.auths import refresh_token
from smart_classroom.BaseUserViews import (user_login, get_user_address)

"""Base User API urls"""

urlpatterns = [
    path('login/', user_login.view, name='user_login'),
    path('refresh_token/', refresh_token, name='refresh_token'),
    path('address/', get_user_address.view, name='get_user_address'),
]
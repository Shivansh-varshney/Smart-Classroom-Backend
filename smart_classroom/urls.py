from .views import *
from django.urls import path
from django.contrib import admin

# import views
from smart_classroom.AdminViews import admin_signup, create_organisation, get_organisation
from smart_classroom.BaseUserViews import user_login

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/admin/signup/', admin_signup.view, name='admin_signup'),
    path('api/user/login/', user_login.view, name='admin_login'),
    path('api/admin/organisation/', get_organisation.view, name='admin_organisation'),
    path('api/admin/organisation/create/', create_organisation.view, name='admin_organisation_create'),
]

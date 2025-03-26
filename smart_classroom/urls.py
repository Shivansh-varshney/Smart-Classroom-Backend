from django.contrib import admin
from django.urls import path, include

# import urls
from smart_classroom.BaseUserViews import urls as baseUserURLS
from smart_classroom.AdminViews import urls as adminURLS

urlpatterns = [
    # django admin
    path('admin/', admin.site.urls),

    # base user apis
    path('api/user/', include(baseUserURLS)),

    # ADMIN APIS
    path('api/admin/', include(adminURLS)),
]
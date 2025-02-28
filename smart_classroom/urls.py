from django.urls import path
from django.contrib import admin

# import views
from smart_classroom.AdminViews import (admin_signup, 
                                        create_organisation, get_organisation,          #organisation views
                                        get_department, create_department,           #department views
                                        create_degree, create_course, create_teacher,
                                        create_student, create_subject
                                        )
from smart_classroom.BaseUserViews import (user_login)

from utils.helpers.auths import refresh_token

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/admin/signup/', admin_signup.view, name='admin_signup'),
    path('api/user/login/', user_login.view, name='admin_login'),
    path('api/user/refresh_token/', refresh_token, name='refresh_token'),
    path('api/admin/organisation/', get_organisation.view, name='get_admin_organisation'),
    path('api/admin/organisation/create/', create_organisation.view, name='create_admin_organisation'),
    path('api/admin/department/', get_department.view, name='get_organisation_department'),
    path('api/admin/department/create/', create_department.view, name='create_organisation_department'),
    path('api/admin/degree/create/', create_degree.view, name='create_department_degree'),
    path('api/admin/course/create/', create_course.view, name='create_degree_course'),
    path('api/admin/subject/create/', create_subject.view, name='create_course_subject'),
    path('api/admin/teacher/create/', create_teacher.view, name='create_teacher'),
    path('api/admin/student/create/', create_student.view, name='create_student'),
]
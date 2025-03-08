from django.urls import path
from django.contrib import admin

# import views
from smart_classroom.AdminViews import (admin_signup, 
                                        create_organisation, get_organisation, update_organisation, # organisation views
                                        get_department, create_department, update_department,  # department views
                                        create_degree, update_degree, create_course, update_course, # degree and course
                                        create_subject, update_subject, create_teacher, update_teacher, # subject and teacher
                                        create_student, create_admin # student and admin
                                        )
from smart_classroom.BaseUserViews import (user_login)

from utils.helpers.auths import refresh_token

urlpatterns = [
    # django admin
    path('admin/', admin.site.urls),

    # base user apis
    path('api/user/login/', user_login.view, name='admin_login'),
    path('api/user/refresh_token/', refresh_token, name='refresh_token'),

    # ADMIN APIS
    path('api/admin/signup/', admin_signup.view, name='admin_signup'),

    # admin organisation
    path('api/admin/organisation/', get_organisation.view, name='get_admin_organisation'),
    path('api/admin/organisation/create/', create_organisation.view, name='create_admin_organisation'),
    path('api/admin/organisation/update/', update_organisation.view, name='update_admin_organisation'),

    # organisation department
    path('api/admin/department/', get_department.view, name='get_organisation_department'),
    path('api/admin/department/create/', create_department.view, name='create_organisation_department'),
    path('api/admin/department/update/', update_department.view, name='update_organisation_department'),
    
    # department degrees
    path('api/admin/degree/create/', create_degree.view, name='create_department_degree'),
    path('api/admin/degree/update/', update_degree.view, name='update_department_degree'),

    # degree courses 
    path('api/admin/course/create/', create_course.view, name='create_degree_course'),
    path('api/admin/course/update/', update_course.view, name='update_degree_course'),

    # course subjects
    path('api/admin/subject/create/', create_subject.view, name='create_course_subject'),
    path('api/admin/subject/update/', update_subject.view, name='update_course_subject'),

    # other admins for organisation
    path('api/admin/other_admin/create/', create_admin.view, name='create_other_admin'),

    # organisation teachers
    path('api/admin/teacher/create/', create_teacher.view, name='create_teacher'),
    path('api/admin/teacher/update/', update_teacher.view, name='update_teacher'),

    # organisation students
    path('api/admin/student/create/', create_student.view, name='create_student'),
]
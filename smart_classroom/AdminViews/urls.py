from django.urls import path
from smart_classroom.AdminViews import (admin_signup, 
                                        create_organisation, get_organisation, update_organisation, # organisation views
                                        get_department, create_department, update_department,  # department views
                                        create_degree, update_degree, create_course, update_course, # degree and course
                                        create_subject, update_subject, create_teacher, update_teacher, # subject and teacher
                                        create_student, create_admin, # student and admin
                                        remove_user, # remove user
                                        create_user_address, update_user_address # user addresses
                                        )

""" Admin API urls"""

urlpatterns = [
    # miscellaneous
    path('signup/', admin_signup.view, name='admin_signup'),
    path('user/remove/', remove_user.view, name='remove_user'),

    # address
    path('address/create/', create_user_address.view, name='create_user_address'),
    path('address/update/', update_user_address.view, name='update_user_address'),

    # admin organisation
    path('organisation/', get_organisation.view, name='get_admin_organisation'),
    path('organisation/create/', create_organisation.view, name='create_admin_organisation'),
    path('organisation/update/', update_organisation.view, name='update_admin_organisation'),

    # organisation department
    path('department/', get_department.view, name='get_organisation_department'),
    path('department/create/', create_department.view, name='create_organisation_department'),
    path('department/update/', update_department.view, name='update_organisation_department'),
    
    # department degrees
    path('degree/create/', create_degree.view, name='create_department_degree'),
    path('degree/update/', update_degree.view, name='update_department_degree'),

    # degree courses 
    path('course/create/', create_course.view, name='create_degree_course'),
    path('course/update/', update_course.view, name='update_degree_course'),

    # course subjects
    path('subject/create/', create_subject.view, name='create_course_subject'),
    path('subject/update/', update_subject.view, name='update_course_subject'),

    # other admins for organisation
    path('other_admin/create/', create_admin.view, name='create_other_admin'),

    # organisation teachers
    path('teacher/create/', create_teacher.view, name='create_teacher'),
    path('teacher/update/', update_teacher.view, name='update_teacher'),

    # organisation students
    path('student/create/', create_student.view, name='create_student'),

]
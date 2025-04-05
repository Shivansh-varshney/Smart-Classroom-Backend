from django.contrib import admin
from .models import *

admin.site.register(User)
admin.site.register(Organisation)
admin.site.register(Department)
admin.site.register(Degree)
admin.site.register(Course)
admin.site.register(Subject)
admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(Result)
admin.site.register(UserAddress)
admin.site.register(ContactRequest)
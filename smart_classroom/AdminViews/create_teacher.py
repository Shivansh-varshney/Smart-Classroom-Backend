import json
import hashlib
from . import verify_admin
from django.db import IntegrityError
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from smart_classroom.models import User, Organisation, Department, Teacher

@csrf_exempt
def view(request):

    if request.method == 'POST':

        try:
            verify = verify_admin.view(request)
            if verify.status_code != 200:
                return verify

            department_id = request.POST.get('department_id')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            phone = request.POST.get('phone')
            email = request.POST.get('email')
            image = request.FILES.get('image') # image file
            salary = request.POST.get('salary')
            password = request.POST.get('password')
            
            if not department_id or not first_name or not last_name or not phone or not email or not image or not salary or not password:
                return JsonResponse({
                    'status': 'error',
                    'message': 'One or more fields missing'
                }, status=403)

            # queries
            adminObj = User.objects.get(id=request.META.get('HTTP_USER_ID'))
            departmentObj = Department.objects.get(id=department_id)

            userObj = User.objects.create(
                organisation=adminObj.organisation,
                first_name=first_name,
                last_name=last_name,
                phone=phone,
                email=email,
                role='teacher',
                password=password
            )
            userObj.save()

            teacherObj = Teacher.objects.create(
                user = userObj,
                department=departmentObj,
                image=image,
                salary=salary
            )
            teacherObj.save()

            return JsonResponse({
                'status': 'success',
                'message': 'Teacher created successfully',
                'teacher': {
                    'user_id': userObj.id,
                    'teacher_id': teacherObj.id
                }
            }, status=201)

        except Department.DoesNotExist:
            return JsonResponse({
                'status': 'error',
                'message': 'Department not found'
            }, status=404)

        except IntegrityError:
            return JsonResponse({
                'status': 'error',
                'message': 'Teacher already exists'
            }, status=401)

    return JsonResponse({
        'status': 'error',
        'message': 'Invalid request method'
    }, status=405)
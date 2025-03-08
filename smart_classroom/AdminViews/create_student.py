import json
from . import verify_admin
from django.db import IntegrityError
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from smart_classroom.models import User, Organisation, Degree, Student

@csrf_exempt
def view(request):

    if request.method =='POST':            
        try:
            verify = verify_admin.view(request)
            if verify.status_code != 200:
                return verify

            degree_id = request.POST.get('degree_id')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            phone = request.POST.get('phone')
            email = request.POST.get('email')
            image = request.FILES.get('image') # image file
            password = request.POST.get('password')
            semester = request.POST.get('semester')
            roll_number = request.POST.get('roll_number')
            category = request.POST.get('category')
            father_name = request.POST.get('father_name')
            mother_name = request.POST.get('mother_name')
            father_occupation = request.POST.get('father_occupation')
            mother_occupation = request.POST.get('mother_occupation')
            parent_phone = request.POST.get('parent_phone')
            parent_email = request.POST.get('parent_email')
            
            if not degree_id or not first_name or not last_name or not phone or not email or not image \
            or not password or not semester or not roll_number or not category or not father_name or not mother_name \
            or not father_occupation or not mother_occupation or not parent_phone or not parent_email:
                return JsonResponse({
                    'status': 'error',
                    'message': 'One or more fields missing'
                }, status=403)

            # queries
            adminObj = User.objects.get(id=request.META.get('HTTP_USER_ID'))
            degreeObj = Degree.objects.get(id=degree_id)

            userObj = User.objects.create(
                organisation = adminObj.organisation,
                first_name=first_name,
                last_name=last_name,
                phone=phone,
                email=email,
                role='student',
                password=password
            )
            userObj.save()

            studentObj = Student.objects.create(
                user=userObj,
                degree=degreeObj,
                image=image,
                semester=semester,
                roll_number=roll_number,
                category=category,
                father_name=father_name,
                mother_name=mother_name,
                father_occupation=father_occupation,
                mother_occupation=mother_occupation,
                parent_phone=parent_phone,
                parent_email=parent_email,
            )

            studentObj.save()

            return JsonResponse({
                'status': 'success',
                'message': 'Student created successfully',
                'student': {
                    'user_id': userObj.id,
                    'student_id': studentObj.id
                }
            }, status=201)

        except Degree.DoesNotExist:
            return JsonResponse({
                'status': 'error',
                'message': 'Degree not found'
            }, status=404)

        except IntegrityError:
            return JsonResponse({
                'status': 'error',
                'message': 'Student already exists'
            }, status=401)

    return JsonResponse({
        'status': 'error',
        'message': 'Invalid request method'
    }, status=405)
import json
from . import verify_admin
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from smart_classroom.models import User, Department, Degree, Course, Teacher

@csrf_exempt
def view(request):

    if request.method == 'POST':

        try:
            verify = verify_admin.view(request)
            if verify.status_code != 200:
                return verify

            data = json.loads(request.body.decode('utf-8'))
            user_id = request.META.get('HTTP_USER_ID')
            department_id = data.get('department_id')

            if not department_id:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Department ID is required'
                }, status=403)

            # queries
            userObj = User.objects.get(id=user_id)
            department = Department.objects.get(id=department_id, organisation__user=userObj)
            degrees = Degree.objects.filter(department=department)
            courses = Course.objects.filter(degree__in=degrees)
            teachers = Teacher.objects.filter(department=department)

            return JsonResponse({
                'status': 'success',
                'message': 'Department found',
                'department': {
                    'id': department.id,
                    'name': department.name,
                    'degrees': [
                        {
                            'id': degree.id,
                            'title': degree.title,
                            'branch': degree.branch,
                            'semesters': degree.semesters
                        }
                        for degree in degrees
                    ],
                    'courses': [
                        {
                            'id': course.id,
                            'name': course.name,
                            'credits': course.total_credits
                        }
                        for course in courses
                    ],
                    'subjects': [
                        {
                            'id': subject.id,
                            'name': subject.name,
                            'semester': subject.semester
                        }
                        for subject in department.subjects.all()
                    ],
                    'teachers': [
                        {
                            'id': teacher.user.id,
                            'first_name': teacher.user.first_name,
                            'last_name': teacher.user.last_name,
                            'phone': teacher.user.phone,
                            'email': teacher.user.email,
                            'image': teacher.image.url,
                            'salary': teacher.salary
                        }
                        for teacher in teachers
                    ]
                }
            }, status=200)

        except Department.DoesNotExist:
            return JsonResponse({
                'status': 'error',
                'message': 'Department not found'
            }, status=404)
        
        except Exception:
            return JsonResponse({
                'status': 'error',
                'message': 'Something went wrong'
            }, status=500)

    return JsonResponse({
        'status': 'error',
        'message': 'Invalid request method'
    }, status=405)
import json
from . import verify_admin
from django.http import JsonResponse
from smart_classroom.models import Degree, Course


def view(request):

    if request.method == 'POST':
        try:

            verify = verify_admin.view(request)
            if verify.status_code != 200:
                return verify

            data = json.loads(request.body.decode('utf-8'))
            degree_id = data.get('degree_id')
            name = data.get('name')
            total_credits = data.get('credits')

            if not degree_id or not name or not total_credits:
                return JsonResponse({
                    'status': 'error',
                    'message': 'one or more fields missing'
                }, status=403)

            # queries
            degreeObj = Degree.objects.get(id=degree_id)
            course = Course.objects.create(
                degree=degreeObj,
                name=name,
                total_credits=total_credits
            )

            course.save()

            return JsonResponse({
                'status': 'success',
                'message': 'Course created successfully',
                'course_id': course.id
            }, status=201)

        except Degree.DoesNotExist:
            return JsonResponse({
                'status': 'error',
                'message': 'Degree does not exist'
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
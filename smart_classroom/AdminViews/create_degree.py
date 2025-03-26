import json
from . import verify_admin
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from smart_classroom.models import User, Department, Degree

@csrf_exempt
def view(request):

    if request.method == 'POST':
        
        try:

            verify = verify_admin.view(request)
            if verify.status_code != 200:
                return verify

            user_id = request.META.get('HTTP_USER_ID')
            data = json.loads(request.body.decode('utf-8'))
            department_id = data.get('department_id')
            title = data.get('title')
            branch = data.get('branch')
            semesters = data.get('semesters')

            if not department_id or not title or not branch or not semesters:
                return JsonResponse({
                    'status': 'error',
                    'message': 'one or more fields missing'
                }, status=403)

            # queries
            userObj = User.objects.get(id=user_id)
            departmentObj = Department.objects.get(id=department_id, organisation__user=userObj)
            degreeObj = Degree.objects.create(
                department=departmentObj,
                title=title,
                branch=branch,
                semesters=semesters
            )

            degreeObj.save()

            return JsonResponse({
                'status': 'success',
                'message': 'Degree created',
                'degree_id': degreeObj.id
            }, status=201)

        except Department.DoesNotExist:
            return JsonResponse({
                'status': 'error',
                'message': 'Department does not exist'
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
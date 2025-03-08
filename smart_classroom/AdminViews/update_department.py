import json
from . import verify_admin
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from smart_classroom.models import Department

@csrf_exempt
def view(request):

    if request.method == "POST":

        try:

            verify = verify_admin.view(request)
            if verify.status_code != 200:
                return verify

            data = json.loads(request.body.decode('utf-8'))
            department_id = data.get('department_id')
            new_details = data.get('new_details')

            if not department_id or not new_details:
                return JsonResponse({
                    'status': 'error',
                    'message': 'one or more fields missing'
                }, status=403)

            # queries
            departmentObj = Department.objects.get(id=department_id)

            for field, value in new_details.items():
                if hasattr(departmentObj, field):
                    if field.lower() == "organisation":
                        return JsonResponse({
                            'status': 'error',
                            'message': 'Organisation of department can not be changed'
                        }, status=403)
                    
                    setattr(departmentObj, field, value)
                else:
                    return JsonResponse({
                        'status': 'error',
                        'message': f'{field} is invalid field'
                    }, status=400)
                
            departmentObj.save()

            return JsonResponse({
                'status': 'success',
                'message': 'Department updated successfully'
            }, status=200)

        except Department.DoesNotExist:
            return JsonResponse({
                'status':'error',
                'message': 'Department not found'
            }, status=404)

        except Exception:
            return JsonResponse({
                    'status': 'error',
                    'message': 'Something went wrong'
                }, status=400)
    
    return JsonResponse({
        'status': 'error',
        'message': 'Invalid request method'
    }, status=405)
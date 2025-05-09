import json
from . import verify_admin
from django.http import JsonResponse
from smart_classroom.models import Organisation, Department


def view(request):
        
    if request.method == 'POST':

        try:

            verify = verify_admin.view(request)
            if verify.status_code != 200:
                return verify

            data = json.loads(request.body.decode('utf-8'))
            organisation_id = data.get('organisation_id')
            name = data.get('name')

            if not organisation_id or not name:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Organisation ID or name missing'
                }, status=403)

            organisationObj = Organisation.objects.get(id=organisation_id)

            department = Department.objects.create(
                organisation=organisationObj,
                name=name
            )

            department.save()

            return JsonResponse({
                'status': 'success',
                'message': 'Department created successfully',
                'department_id': department.id
            }, status=201)

        except Organisation.DoesNotExist:
            return JsonResponse({
                'status': 'error',
                'message': 'Organisation not found'
            }, status=404)
        
        except Exception:
            return JsonResponse({
                'status': 'error',
                'message': 'Something went wrong'
            }, status=500)

    return JsonResponse({
        'status': 'error',
        'message': 'Invalid Request Method'
    }, status=405)
import json
from . import verify_admin
from django.http import JsonResponse
from smart_classroom.models import Degree


def view(request):
    if request.method == "POST":

        try:

            verify = verify_admin.view(request)
            if verify.status_code != 200:
                return verify

            data = json.loads(request.body.decode('utf-8'))
            degree_id = data.get('degree_id')
            new_details = data.get('new_details')

            if not degree_id or not new_details:
                return JsonResponse({
                    'status': 'error',
                    'message': 'one or more fields missing'
                }, status=403)

            # queries
            degreeObj = Degree.objects.get(id=degree_id)

            for field, value in new_details.items():
                if hasattr(degreeObj, field):
                    if field.lower() == 'department':
                        return JsonResponse({
                            'status': 'error',
                            'message': 'Department of a degree can not be changed'
                        }, status=403)

                    setattr(degreeObj, field, value)

                else:
                    return JsonResponse({
                        'status': 'error',
                        'message': f'{field} is invalid field'
                    }, status=400)

            degreeObj.save()

            return JsonResponse({
                'status': 'success',
                'message': 'Degree updated successfully'
            }, status=200)

        except Degree.DoesNotExist:
            return JsonResponse({
                'status':'error',
                'message': 'Degree not found'
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
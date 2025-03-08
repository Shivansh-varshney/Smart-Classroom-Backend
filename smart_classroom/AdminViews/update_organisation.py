import json
from . import verify_admin
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from smart_classroom.models import User, Organisation

@csrf_exempt
def view(request):

    if request.method == "POST":

        try:

            verify = verify_admin.view(request)
            if verify.status_code != 200:
                return verify
                
            data = json.loads(request.body.decode('utf-8'))
            new_details = data.get('new_details')
            user_id = request.META.get('HTTP_USER_ID')

            if not new_details:
                return JsonResponse({
                'status': 'error',
                'message': 'new_details field missing'
            }, status=403)

            # Queries
            adminObj = User.objects.get(id=user_id)
            organisationObj = adminObj.organisation

            for field, value in new_details.items():
                if hasattr(organisationObj, field):
                    setattr(organisationObj, field, value)
                
                else:
                    return JsonResponse({
                        'status': 'error',
                        'message': f'{field} is invalid field'
                    }, status=400)

            organisationObj.save()

            return JsonResponse({
                'status': 'success',
                'message': 'Organisation updated successfully'
            }, status=200)

        except Exception:
            return JsonResponse({
                'status': 'error',
                'message': 'Something went wrong'
            }, status=400)
    
    return JsonResponse({
        'status': 'error',
        'message': 'Invalid request method'
    }, status=405)
import json
from . import verify_admin
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from smart_classroom.models import UserAddress

@csrf_exempt
def view(request):

    if request.method == "POST":

        try:

            verify = verify_admin.view(request)
            if verify.status_code != 200:
                return verify

            data = json.loads(request.body.decode('utf-8'))
            address_id = data.get('address_id')
            new_details = data.get('new_details')

            if not address_id or not new_details:
                return JsonResponse({
                    'status': 'error',
                    'message': 'one or more fields missing'
                }, status=403)

            # queries
            addressObj = UserAddress.objects.get(id=address_id)

            for field, value in new_details.items():
                if hasattr(addressObj, field):
                    if field.lower() == 'user_id' or field.lower() == "user":
                        return JsonResponse({
                            'status': 'error',
                            'message': 'User can not be changed'
                        }, status=403)
                    
                    setattr(addressObj, field, value)

                else:
                    return JsonResponse({
                        'status': 'error',
                        'message': f'{field} is invalid field'
                    }, status=400)

            addressObj.save()

            return JsonResponse({
                'status': 'success',
                'message': 'Address updated successfully'
            }, status=200)

        except UserAddress.DoesNotExist:
            return JsonResponse({
                'status': 'error',
                'message': 'Address not found'
            }, status=404)

    return JsonResponse({
        'status': 'error',
        'message': 'Invalid request method'
    }, status=405)
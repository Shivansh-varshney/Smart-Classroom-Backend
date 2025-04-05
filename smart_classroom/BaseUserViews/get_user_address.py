import json
from django.http import JsonResponse
from smart_classroom.models import User, UserAddress


def view(request):

    if request.method == 'POST':
        try:

            data = json.loads(request.body.decode('utf-8'))
            user_id = data.get('user_id')

            if not user_id:
                return JsonResponse({
                    'status': 'error',
                    'message': 'user_id is missing'
                }, status=403)

            # queries
            userObj = User.objects.get(id=user_id)
            addressObj = UserAddress.objects.get(user=userObj)

            return JsonResponse({
                'status': 'success',
                'message': 'User address found',
                'address': {
                    'id': addressObj.id,
                    'house_number': addressObj.house_number,
                    'street': addressObj.street,
                    'city': addressObj.city,
                    'district': addressObj.district,
                    'state': addressObj.state,
                    'country': addressObj.country,
                    'zipcode': addressObj.zipcode
                }
            }, status=200)

        except UserAddress.DoesNotExist:
            return JsonResponse({
                'status': 'error',
                'message': 'User does not have address'
            }, status=401)

        except User.DoesNotExist:
            return JsonResponse({
                'status': 'error',
                'message': 'User not found'
            }, status=404)

    return JsonResponse({
        'status': 'error',
        'message': 'Invalid request method'
    }, status=405)
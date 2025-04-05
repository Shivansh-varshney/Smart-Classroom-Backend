import json
from . import verify_admin
from django.db import IntegrityError
from django.http import JsonResponse
from smart_classroom.models import User, UserAddress


def view(request):

    if request.method == 'POST':
        try:

            verify = verify_admin.view(request)
            if verify.status_code != 200:
                return verify

            data = json.loads(request.body.decode('utf-8'))
            user_id = data.get('user_id')
            house_number = data.get('house_number')
            street = data.get('street')
            city = data.get('city')
            district = data.get('district')
            state = data.get('state')
            country = data.get('country')
            zipcode = data.get('zipcode')

            if not user_id or not house_number or not street or not city \
            or not district or not state or not country or not zipcode:
                return JsonResponse({
                        'status': 'error',
                        'message': 'one or more fields missing'
                    }, status=403)

            # queries
            userObj = User.objects.get(id=user_id)

            addressObj = UserAddress.objects.create(
                user=userObj,
                house_number=house_number,
                street=street,
                city=city,
                district=district,
                state=state,
                country=country,
                zipcode=zipcode
            )

            return JsonResponse({
                'status': 'success',
                'message': 'Address saved successfully',
                'address_id': addressObj.id
            }, status=201)

        except User.DoesNotExist:
            return JsonResponse({
                'status': 'error',
                'message': 'User not found'
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
import json
from . import verify_admin
from django.db import IntegrityError
from django.http import JsonResponse
from smart_classroom.models import User, Organisation

def view(request):

    if request.method == "POST":
        try:
            verify = verify_admin.view(request)
            if verify.status_code != 200:
                return verify
                
            data = json.loads(request.body.decode('utf-8'))
            first_name = data.get('first_name')
            last_name = data.get('last_name')
            phone = data.get('phone')
            email = data.get('email')
            role = 'admin'

            if not first_name or not last_name or not phone or not email:
                return JsonResponse({
                    'status': 'error',
                    'message': 'one or more fields missing'
                }, status=403)

            # queries
            adminObj = User.objects.get(id=request.META.get('HTTP_USER_ID'))
            userObj = User.objects.create(
                organisation=adminObj.organisation,
                first_name=first_name,
                last_name=last_name,
                phone=phone,
                email=email
            )
            
            return JsonResponse({
                'status': 'success',
                'message': 'admin added successfully'
            }, status=201)

        except IntegrityError:
            return JsonResponse({
                'status': 'error',
                'message': 'Admin already exists'
            }, status=401)
        
        except Exception:
            return JsonResponse({
                'status': 'error',
                'message': 'Something went wrong'
            }, status=500)

    return JsonResponse({
        'status': 'error',
        'message': 'Invalid request method'
    }, status=405)

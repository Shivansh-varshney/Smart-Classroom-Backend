import json
import hashlib
from django.http import JsonResponse
from smart_classroom.models import User


def view(request):
        if request.method == 'POST':
            data = json.loads(request.body.decode('utf-8'))
            first_name = data.get('first_name')
            last_name = data.get('last_name')
            phone = data.get('phone')
            email = data.get('email')
            password = data.get('password')
            role = 'admin'

            if not first_name or not last_name or not phone or not email or not password:
                return JsonResponse({
                    'status': 'error',
                    'message': 'One or more details missing'
                }, status=403)

            try:
                userObj = User.objects.get(email=email)
                return JsonResponse({
                    'status': 'error',
                    'message': 'Email already in use'
                }, status=403)     

            except User.DoesNotExist:

                userObj = User.objects.create(
                    first_name=first_name,
                    last_name=last_name,
                    phone=phone,
                    email=email,
                    password=hashlib.sha256(password.encode()).hexdigest()
                )
                userObj.save()
                return JsonResponse({
                    'status': 'success',
                    'message': 'Admin registered'
                }, status=201)

        return JsonResponse({
                'status': 'error',
                'message': 'Invalid request method'
            }, status=405
        )

import json
import hashlib
from django.http import JsonResponse
from smart_classroom.models import User
from utils.helpers.auths import generate_token
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def view(request):

    if request.method == 'POST':
        
        data = json.loads(request.body.decode('utf-8'))
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return JsonResponse({
                'status': 'error',
                'message': 'Credentials incomplete'
            }, status=403)
        
        try:
            userObj = User.objects.get(email=email)

            user_email = userObj.email
            user_password = userObj.password

            if user_email == email and user_password == hashlib.sha256(password.encode()).hexdigest():

                token = generate_token(userObj)

                response = JsonResponse({
                    'status': 'success',
                    'message': 'login successful',
                    'user': {
                        'id': userObj.id,
                        'first_name': userObj.first_name,
                        'last_name': userObj.last_name,
                        'email': userObj.email,
                        'phone': userObj.phone
                    }
                }, status=200)

                response['USER-ID'] = userObj.id
                response['AUTHORIZATION'] = token

                return response
            
            return JsonResponse({
                'status': 'error',
                'message': f"Wrong password"
            }, status=403)
        
        except User.DoesNotExist:
            return JsonResponse({
                'status': 'error',
                'message': 'Email not found'
            }, status=404)
        
    return JsonResponse({
            'status': 'error',
            'message': 'Invalid request method'
        }, status=405
    )

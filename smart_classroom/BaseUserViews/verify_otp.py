import json
import random
import hashlib
from django.http import JsonResponse
from smart_classroom.models import User, EmailOTP
from utils.helpers.auths import generate_token

def view(request):

    if request.method == 'POST':
        
        data = json.loads(request.body.decode('utf-8'))
        email = data.get('email')
        otp = data.get('otp')
        
        if not email or not otp:
            return JsonResponse({
                'status': 'error',
                'message': 'Credentials incomplete'
            }, status=403)
        
        try:
            # queries
            otpObj = EmailOTP.objects.filter(email=email).latest('createdAt')
            userObj = User.objects.get(email=email)

            if otpObj.otp == hashlib.sha256(str(otp).encode()).hexdigest():
                otpObj.delete()
                tokens = generate_token(userObj)

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
                response['ACCESS-TOKEN'] = tokens['access_token']
                response['REFRESH-TOKEN'] = tokens['refresh_token']

                return response

        except EmailOTP.DoesNotExist:
            return JsonResponse({
                'status': 'error',
                'message': 'OTP not verified'
            }, status=403)

        except Exception as error:
            return JsonResponse({
                'status': 'error',
                'message': f'Error: {error}'
            }, status=500)
        
    return JsonResponse({
            'status': 'error',
            'message': 'Invalid request method'
        }, status=405
    )
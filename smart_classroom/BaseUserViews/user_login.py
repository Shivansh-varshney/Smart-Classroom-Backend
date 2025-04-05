import json
import random
import hashlib
from django.http import JsonResponse
from django.core.mail import send_mail
from smart_classroom.models import User, EmailOTP

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

                subject = "OTP for classflow login."
                otp = str(random.randint(1000000, 9999999))
                message = f"Use {otp} as the one-time password to login the classlow dashboard."
                from_email = None
                recipient_list = [userObj.email]
                send_mail(subject, message, from_email, recipient_list)
                EmailOTP.objects.create(
                    email=userObj.email,
                    otp=hashlib.sha256(otp.encode()).hexdigest()
                )

                return JsonResponse({
                    'status': 'success',
                    'message': 'OTP sent successfully'
                }, status = 200)
            
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

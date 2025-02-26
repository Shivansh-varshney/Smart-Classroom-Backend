import jwt
import datetime
from django.http import JsonResponse
from django.conf import settings

def generate_token(user):

    payload = {
        'user_id': user.id,
        'exp': int((datetime.datetime.utcnow() + datetime.timedelta(seconds=settings.JWT_EXPIRATION_SECONDS)).timestamp()),
        'iat': int(datetime.datetime.utcnow().timestamp())
    }

    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM)

def verify_token(token):

    try:
        token = jwt.decode(token, settings.SECRET_KEY, algorithms=settings.JWT_ALGORITHM)
        if token:
            return JsonResponse({
                'status': 'success',
                'token': token,
                'message': 'Valid User'
            }, status=200)

    except jwt.ExpiredSignatureError:
        return JsonResponse({
            'status': 'error',
            'message': 'Token expired'
        }, status=400)

    except jwt.InvalidTokenError:
        return JsonResponse({
            'status': 'error',
            'message': 'Invalid Token'
        }, status=400)
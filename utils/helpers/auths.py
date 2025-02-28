import jwt
import datetime
from django.http import JsonResponse
from django.conf import settings

def generate_token(user):

    access_payload = {
        'user_id': user.id,
        'exp': int((datetime.datetime.utcnow() + datetime.timedelta(seconds=settings.JWT_EXPIRATION_SECONDS)).timestamp()),
        'iat': int(datetime.datetime.utcnow().timestamp())
    }

    access_token = jwt.encode(access_payload, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    
    refresh_payload = {
        'user_id': user.id,
        'exp': int((datetime.datetime.utcnow() + datetime.timedelta(days=settings.JWT_REFRESH_EXPIRATION_DAYS)).timestamp()),
        'iat': int(datetime.datetime.utcnow().timestamp())
    }
    refresh_token = jwt.encode(refresh_payload, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM)

    return {
        'access_token': access_token,
        'refresh_token': refresh_token
    }

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
        }, status=401)

    except jwt.InvalidTokenError:
        return JsonResponse({
            'status': 'error',
            'message': 'Invalid Token'
        }, status=401)

def refresh_token(request):

    try:
        refresh_token = request.META.get("HTTP_REFRESH_TOKEN")
        user_id = request.META.get("HTTP_USER_ID")
        token = jwt.decode(refresh_token, settings.SECRET_KEY, algorithms=settings.JWT_ALGORITHM)
        if token:

            access_payload = {
                'user_id': user_id,
                'exp': int((datetime.datetime.utcnow() + datetime.timedelta(seconds=settings.JWT_EXPIRATION_SECONDS)).timestamp()),
                'iat': int(datetime.datetime.utcnow().timestamp())
            }

            access_token = jwt.encode(access_payload, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
            return JsonResponse({
                'status': 'success',
                'access_token': access_token,
                'message': 'Valid User'
            }, status=200)

    except jwt.ExpiredSignatureError:
        return JsonResponse({
            'status': 'error',
            'message': 'Refresh token expired'
        }, status=401)

    except jwt.InvalidTokenError:
        return JsonResponse({
            'status': 'error',
            'message': 'Invalid refresh token'
        }, status=401)
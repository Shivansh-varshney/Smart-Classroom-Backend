import jwt
import datetime
from django.conf import settings

def generate_token(user):

    payload = {
        'user_id': user.id,
        'expire': datetime.datetime.utcnow() + datetime.timedelta(seconds=settings.JWT_EXPIRATION_SECONDS),
        'iat': datetime.datetime.utcnow()
    }

    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM)

def verify_token(token):

    try:
        return jwt.decode(token, settings.SECRET_KEY, algorithms=settings.JWT_ALGORITHM)

    except jwt.ExpiredSignatureError:
        return False
    except jwt.InvalidTokenError:
        return None
    
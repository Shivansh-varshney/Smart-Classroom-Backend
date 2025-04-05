from django.http import JsonResponse
from smart_classroom.models import User
from smart_classroom.BaseUserViews import verify_session


def view(request):

    verify = verify_session.view(request)
    if verify.status_code != 200:
        return verify

    user_id = request.META.get('HTTP_USER_ID')
    try:
        userObj = User.objects.get(id=user_id)
        if userObj.role == 'admin':
            return JsonResponse({
                'status': 'success'
            }, status=200)
        
        return JsonResponse({
            'status': 'error',
            'message': 'unauthorized access'
        }, status=401)
    
    except User.DoesNotExist:
        return JsonResponse({
            'status': 'error',
            'message': 'unauthorized access'
        }, status=401)
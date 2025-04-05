import json
from django.http import JsonResponse
from smart_classroom.models import User
from django.middleware.csrf import get_token
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def view(request):

    if request.method == "GET":
        response = JsonResponse({
            'status': 'success',
            'message': 'CSRF cookie set'
        }, status=200)

        response['X_CSRFToken'] = get_token(request)
        
        return response
    
    return JsonResponse({
        'status': 'error',
        'message': 'Invalid request method'
    }, status=405)
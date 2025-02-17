from django.http import JsonResponse
from utils.helpers.auths import verify_token
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def view(request):

    auth_header = request.META.get('HTTP_AUTHORIZATION')
    if auth_header and auth_header.startswith('Bearer '):
        token = auth_header.split(' ')[1]
        return verify_token(token)
        
    return JsonResponse({
        'status': 'error',
        'message': 'Authentication header missing'
    })
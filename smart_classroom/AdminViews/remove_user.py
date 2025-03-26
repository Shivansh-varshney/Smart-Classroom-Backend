import json
import hashlib
from . import verify_admin
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from smart_classroom.models import User

@csrf_exempt
def view(request):

    if request.method == 'POST':

        try:
            verify = verify_admin.view(request)
            if verify.status_code != 200:
                return verify

            data = json.loads(request.body.decode('utf-8'))
            user_id = data.get('user_id')

            if not user_id:
                return JsonResponse({
                    'status': 'error',
                    'message': 'user_id is required'
                }, status=403)

            # queries
            userObj = User.objects.get(id = user_id)

            userObj.delete()

            return JsonResponse({
                'status': 'success',
                'message': 'User deleted successfully'
            }, status=200)
        
        except User.DoesNotExist:
            return JsonResponse({
                'status': 'error',
                'message': 'User not found'
            }, status=404)
        
        except Exception:
            return JsonResponse({
                'status': 'error',
                'message': 'Something went wrong'
            }, status=401)
        
    return JsonResponse({
        'status': 'error',
        'message': 'Invalid request method'
    }, status=405)
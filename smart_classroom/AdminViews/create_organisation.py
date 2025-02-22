import json
from . import verify_admin
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from smart_classroom.models import User, Organisation

@csrf_exempt
def view(request):

    if request.method == 'POST':

        verify = verify_admin.view(request)
        if verify.status_code != 200:
            return verify

        data = json.loads(request.body.decode('utf-8'))
        orgname = data.get('name')
        orgtype = data.get('type')
        orgboard = data.get('board')

        user_id = request.META.get('HTTP_USER_ID')
        userObj = User.objects.get(id=user_id)

        try:
            orgObj = Organisation.objects.get(user=userObj)

            return JsonResponse({
                'status': 'error',
                'message': 'User already has an organisation.'
            }, status=401)

        except Organisation.DoesNotExist:
            if not orgname or not orgtype:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Name and type are required'
                }, status=400)
            
            orgObj = Organisation.objects.create(user=userObj, name=orgname, orgType=orgtype, board=orgboard)
            orgObj.save()

            return JsonResponse({
                'status': 'success',
                'message': 'Organisation created successfully',
                'organisation': {
                    'id': orgObj.id,
                    'name': orgObj.name,
                    'type': orgObj.orgType,
                    'board': orgObj.board,
                    'departments': None
                }
            }, status=201)

    return JsonResponse({
        'status': 'error',
        'message': 'Invalid request method',
    }, status=401)
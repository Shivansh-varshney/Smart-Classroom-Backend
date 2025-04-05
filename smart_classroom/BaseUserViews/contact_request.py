import json
from django.http import JsonResponse
from smart_classroom.models import User, ContactRequest

def view(request):

    if request.method == 'POST':
        try:

            data = json.loads(request.body.decode('utf-8'))
            user_id = data.get("user_id")
            email = data.get("email")
            phone = data.get("phone")
            topic = data.get("topic")
            description = data.get("description")

            if not user_id or not email or not phone or not topic or not description:
                return JsonResponse({
                    'status': 'error',
                    'message': 'one or more fields missing'
                }, status=403)

            # queries
            userObj = User.objects.get(id=user_id)

            contactRequestObj = ContactRequest.objects.create(
                user=userObj,
                email=email,
                phone=phone,
                topic=topic,
                description=description
            )

            return JsonResponse({
                'status': 'success',
                'message': 'Request created successfully',
                'requestID': contactRequestObj.requestID
            }, status=200)
        
        except User.DoesNotExist:
            return JsonResponse({
                'status': 'error',
                'message': 'User not found'
            }, status=404)

    return JsonResponse({
        'status': 'error',
        'message': 'Invalid request method'
    }, status=405)
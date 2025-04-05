import json
from . import verify_admin
from django.http import JsonResponse
from smart_classroom.models import Course


def view(request):

    if request.method == "POST":

        verify = verify_admin.view(request)
        if verify.status_code != 200:
            return verify

        try: 
            data = json.loads(request.body.decode('utf-8'))
            course_id = data.get('course_id')
            new_details = data.get('new_details')

            if not course_id or not new_details:
                return JsonResponse({
                    'status': 'error',
                    'message': 'one or more fields missing'
                }, status=403)

            # queries
            courseObj = Course.objects.get(id=course_id)
            
            for field, value in new_details.items():
                if hasattr(courseObj, field):
                    if field.lower() == 'degree':
                        return JsonResponse({
                            'status': 'error',
                            'message': 'Degree can not be changed'
                        }, status=403)

                    setattr(courseObj, field, value)

                else:
                    return JsonResponse({
                            'status': 'error',
                            'message': f'{field} is invalid field'
                        }, status=400)

            courseObj.save()

            return JsonResponse({
                'status': 'success',
                'message': 'Course updated successfully'
            }, status=200)
        
        except Course.DoesNotExist:
            return JsonResponse({
                'status': 'error',
                'message': 'Course not found'
            }, status=404)

    return JsonResponse({
        'status': 'error',
        'message': 'Invalid request method'
    }, status=405)
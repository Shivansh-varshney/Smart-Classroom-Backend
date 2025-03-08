import json
from . import verify_admin
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from smart_classroom.models import Subject

@csrf_exempt
def view(request):

    if request.method == "POST":

        try:

            verify = verify_admin.view(request)
            if verify.status_code != 200:
                return verify

            data = json.loads(request.body.decode('utf-8'))
            subject_id = data.get('subject_id')
            new_details = data.get('new_details')

            # queries
            subjectObj = Subject.objects.get(id=subject_id)

            for field, value in new_details.items():
                if hasattr(subjectObj, field):
                    if field.lower() == 'course':
                        return JsonResponse({
                            'status': 'error',
                            'message': 'Course can not be changed'
                        }, status=403)
                    
                    setattr(subjectObj, field, value)

                else:
                    return JsonResponse({
                        'status': 'error',
                        'message': f'{field} is invalid field'
                    }, status=400)

            subjectObj.save()

            return JsonResponse({
                'status': 'success',
                'message': 'Subject updated successfully'
            }, status=200)

        except Subject.DoesNotExist:
            return JsonResponse({
                'status': 'error',
                'message': 'Subject not found'
            }, status=404)

        except Exception:
            return JsonResponse({
                'status': 'error',
                'message': 'Something went wrong'
            }, status=400)

    return JsonResponse({
        'status': 'error',
        'message': 'Invalid request method'
    }, status=405)
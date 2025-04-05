import json
from . import verify_admin
from django.http import JsonResponse
from smart_classroom.models import User, Teacher


def view(request):

    if request.method == "POST":

        try:

            verify = verify_admin.view(request)
            if verify.status_code != 200:
                return verify

            data = json.loads(request.body.decode('utf-8'))
            user_id = data.get('user_id')
            new_details = data.get('new_details')

            if not user_id or not new_details:
                return JsonResponse({
                    'status': 'error',
                    'message': 'one or more fields missing'
                }, status=403)

            # queries
            userObj = User.objects.get(id=user_id)
            teacherObj = Teacher.objects.get(user=userObj)

            for field, value in new_details.items():

                valid_fields = ['phone', 'email', 'salary']

                if hasattr(userObj, field) and field.lower() in valid_fields:
                    setattr(userObj, field, value)
                
                elif hasattr(teacherObj, field) and field.lower() in valid_fields:
                    setattr(teacherObj, field, value)
                
                else:
                    return JsonResponse({
                        'status': 'error',
                        'message': f'{field} is invalid field'
                    }, status=400)
                
            userObj.save() 
            teacherObj.save()

            return JsonResponse({
                'status': 'success',
                'message': 'Teacher updated successfully'
            }, status=200)

        except User.DoesNotExist:
            return JsonResponse({
                'status': 'error',
                'message': 'Teacher not found'
            }, status=404)

        except Teacher.DoesNotExist:
            return JsonResponse({
                'status': 'error',
                'message': 'User is not a teacher'
            }, status=400)
        
        except Exception as error:
            return JsonResponse({
                'status': 'error',
                'message': 'Something went wrong'
            }, status=500)
    
    return JsonResponse({
        'status': 'error',
        'message': 'Invalid request method'
    }, status=405)
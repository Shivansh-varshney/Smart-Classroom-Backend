import json
from . import verify_admin
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from smart_classroom.models import Department, Course, Subject, Teacher

@csrf_exempt
def view(request):

    if request.method == 'POST':
        try:

            verify = verify_admin.view(request)
            if verify.status_code != 200:
                return verify

            data = json.loads(request.body.decode('utf-8'))
            department_id = data.get('department_id')
            course_id = data.get('course_id')
            teacher_id = data.get('teacher_id')
            name = data.get('name')
            semester = data.get('semester')

            if not course_id or not name or not semester:
                return JsonResponse({
                    'status': 'error',
                    'message': 'one or more fields missing'
                }, status=403)

            # queries
            courseObj = Course.objects.get(id=course_id)
            departmentObj = Department.objects.get(id=department_id)
            teacherObj = Teacher.objects.get(id=teacher_id) if teacher_id else None

            subject = Subject.objects.create(
                name=name,
                semester=semester
            )
            subject.course.set([courseObj])
            if teacherObj is not None:
                subject.teacher.set([teacherObj])
            subject.save()
            departmentObj.subjects.set([subject])

            return JsonResponse({
                'status': 'success',
                'message': 'Subject created successfully',
                'subject': {
                    'id': subject.id,
                    'name': subject.name,
                }
            }, status=201)

        except Course.DoesNotExist:
            return JsonResponse({
                'status': 'error',
                'message': 'Course not found'
            }, status=404)

        except Teacher.DoesNotExist:
            return JsonResponse({
                'status': 'error',
                'message': 'Teacher not found'
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
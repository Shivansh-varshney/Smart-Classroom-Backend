from . import verify_admin
from django.http import JsonResponse
from django.db.models import Count, Q
from smart_classroom.models import User, Organisation, Department


def view(request):

    if request.method == 'POST':
        
        try:

            verify = verify_admin.view(request)
            if verify.status_code != 200:
                return verify

            user_id = request.META.get('HTTP_USER_ID')
            userObj = User.objects.get(id=user_id)
            orgObj = Organisation.objects.get(user=userObj)
            departments = Department.objects.filter(organisation=orgObj).annotate(
        degree_count=Count('degree', distinct=True),
        course_count=Count('degree__course', distinct=True),
        subject_count=Count('subjects', distinct=True),
        teacher_count=Count('teacher', distinct=True)
    )
            
            return JsonResponse({
                'status': 'success',
                'message': 'Organisation found',
                'organisation': {
                    'org_id': orgObj.id,
                    'name': orgObj.name,
                    'type': orgObj.orgType,
                    'board': orgObj.board,
                    'departments': [
                        {
                            'id': department.id,
                            'name': department.name,
                            'total_degrees': department.degree_count,
                            'total_courses': department.course_count,
                            'total_subjects': department.subject_count,
                            'total_teachers': department.teacher_count
                        } for department in departments
                    ]
                }
            })

        except Organisation.DoesNotExist:

            return JsonResponse({
                'status': 'success',
                'message': 'No organisation',
                'organisation': None
            }, status=200)
    
    return JsonResponse({
        'status': 'error',
        'message': 'Invalid request method'
    }, status=405)
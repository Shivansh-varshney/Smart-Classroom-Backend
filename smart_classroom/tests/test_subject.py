import json
import hashlib
from .TestData import APITestData
from smart_classroom.models import EmailOTP

class SubjectAPITests(APITestData):

    def test_01_create_subject(self):
        """Test create subject"""

        response = self.client.post("/api/admin/subject/create/", {
                "department_id": self.department.id,
                "course_id": self.course.id,            
                "teacher_id": self.teacher.id,            
                "name": "C++ Basics",            
                "semester": 1,        
        }, content_type='application/json')

        self.assertEqual(response.status_code, 201)
        self.assertIn("Subject created successfully", response.content.decode())

    def test_02_create_subject_with_incomplete_details(self):
        """Test create subject with incomplete details"""

        response = self.client.post("/api/admin/subject/create/", {
                "department_id": self.department.id,
                "course_id": self.course.id,            
                "teacher_id": self.teacher.id,            
                "name": "C++ Basics", 
        }, content_type='application/json')

        self.assertEqual(response.status_code, 403)
        self.assertIn("one or more fields missing", response.content.decode())
    
    def test_03_create_subject_without_teacher(self):
        """Test create subject with incomplete details"""

        response = self.client.post("/api/admin/subject/create/", {
                "department_id": self.department.id,
                "course_id": self.course.id,        
                "name": "C++ Basics",
                "semester": 1, 
        }, content_type='application/json')

        self.assertEqual(response.status_code, 201)
        self.assertIn("Subject created successfully", response.content.decode())
    
    def test_04_create_subject_with_invalid_teacher(self):
        """Test create subject with incomplete details"""

        response = self.client.post("/api/admin/subject/create/", {
                "department_id": self.department.id,
                "course_id": self.course.id,
                "teacher_id": 99,       
                "name": "C++ Basics", 
                "semester": 1,
        }, content_type='application/json')

        self.assertEqual(response.status_code, 404)
        self.assertIn("Teacher not found", response.content.decode())
    
    def test_05_create_subject_with_invalid_course(self):
        """Test create subject with incomplete details"""

        response = self.client.post("/api/admin/subject/create/", {
                "department_id": self.department.id,
                "course_id": 99,
                "teacher_id": self.teacher.id,       
                "name": "C++ Basics", 
                "semester": 1,
        }, content_type='application/json')

        self.assertEqual(response.status_code, 404)
        self.assertIn("Course not found", response.content.decode())

    def test_06_create_subject_with_invalid_request_method(self):
        """Test create subject"""

        response = self.client.get("/api/admin/subject/create/", {
                "department_id": self.department.id,
                "course_id": self.course.id,            
                "teacher_id": self.teacher.id,            
                "name": "C++ Basics",            
                "semester": 1,        
        }, content_type='application/json')

        self.assertEqual(response.status_code, 405)
        self.assertIn("Invalid request method", response.content.decode())

    def test_07_create_subject_with_invalid_admin(self):
        """Test create subject"""

        self.otp = EmailOTP.objects.create(email='testuser3@gmail.com', otp=hashlib.sha256('000111'.encode()).hexdigest())

        response = self.client.post('/api/user/verify-otp/', 
        data = {
            'email': 'testuser3@gmail.com',
            'otp': '000111'
        }, content_type='application/json')

        self.token = f"Bearer {response.headers.get('ACCESS-TOKEN')}"
        if self.token:
            self.client.defaults['HTTP_AUTHORIZATION'] = self.token
            self.client.defaults['HTTP_USER_ID'] = str(self.user3.id)

        response = self.client.post("/api/admin/subject/create/", {
                "department_id": self.department.id,
                "course_id": self.course.id,            
                "teacher_id": self.teacher.id,            
                "name": "C++ Basics",            
                "semester": 1,        
        }, content_type='application/json')

        self.assertEqual(response.status_code, 401)
        self.assertIn("unauthorized access", response.content.decode())
    
    def test_08_create_subject_for_unhandled_exceptions(self):
        """Test create subject for unhandled exceptions"""

        response = self.client.post("/api/admin/subject/create/", {
               """"department_id": self.department.id,
                "course_id": self.course.id,            
                "teacher_id": self.teacher.id,            
                "name": "C++ Basics",            
                "semester": 1"""   
        }, content_type='application/json')

        self.assertEqual(response.status_code, 500)
        self.assertIn("Something went wrong", response.content.decode())
    
    def test_09_update_subject_name(self):
        """Test update subject name"""

        response = self.client.post("/api/admin/subject/update/", {
            'subject_id': self.subject.id,
            'new_details': {
                'name': 'New subject name'
            }
        }, content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertIn("Subject updated successfully", response.content.decode())
    
    def test_10_update_subject_semester(self):
        """Test update subject semester"""

        response = self.client.post("/api/admin/subject/update/", {
            'subject_id': self.subject.id,
            'new_details': {
                'semester': 4
            }
        }, content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertIn("Subject updated successfully", response.content.decode())
    
    def test_11_update_subject_invalid_field(self):
        """Test update subject invalid field"""

        response = self.client.post("/api/admin/subject/update/", {
            'subject_id': self.subject.id,
            'new_details': {
                'invalid field': 4
            }
        }, content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertIn("invalid field is invalid field", response.content.decode())
    
    def test_12_update_subject_with_invalid_request_method(self):
        """Test update subject invalid request method"""

        response = self.client.get("/api/admin/subject/update/", {
            'subject_id': self.subject.id,
            'new_details': {
                'semester': 4
            }
        }, content_type='application/json')

        self.assertEqual(response.status_code, 405)
        self.assertIn("Invalid request method", response.content.decode())
    
    def test_13_update_subject_with_invalid_admin(self):
        """Test update subject invalid admin"""

        self.otp = EmailOTP.objects.create(email='testuser3@gmail.com', otp=hashlib.sha256('000111'.encode()).hexdigest())

        response = self.client.post('/api/user/verify-otp/', 
        data = {
            'email': 'testuser3@gmail.com',
            'otp': '000111'
        }, content_type='application/json')

        self.token = f"Bearer {response.headers.get('ACCESS-TOKEN')}"
        if self.token:
            self.client.defaults['HTTP_AUTHORIZATION'] = self.token
            self.client.defaults['HTTP_USER_ID'] = str(self.user3.id)

        response = self.client.post("/api/admin/subject/update/", {
            'subject_id': self.subject.id,
            'new_details': {
                'semester': 4
            }
        }, content_type='application/json')

        self.assertEqual(response.status_code, 401)
        self.assertIn("unauthorized access", response.content.decode())
    
    def test_14_update_non_existent_subject(self):
        """Test update non existent subject"""

        response = self.client.post("/api/admin/subject/update/", {
            'subject_id': 99,
            'new_details': {
                'semester': 4
            }
        }, content_type='application/json')

        self.assertEqual(response.status_code, 404)
        self.assertIn("Subject not found", response.content.decode())
    
    def test_15_update_subject_unhandled_exceptions(self):
        """Test update subject unhandled exceptions"""

        response = self.client.post("/api/admin/subject/update/", {
            """'subject_id': self.subject.id,
            'new_details': {
                'semester': 4
            }"""
        }, content_type='application/json')

        self.assertEqual(response.status_code, 500)
        self.assertIn("Something went wrong", response.content.decode())

    def test_16_update_subject_course(self):
        """Test update subject name"""

        response = self.client.post("/api/admin/subject/update/", {
            'subject_id': self.subject.id,
            'new_details': {
                'course': 'New course name'
            }
        }, content_type='application/json')

        self.assertEqual(response.status_code, 403)
        self.assertIn("Course can not be changed", response.content.decode())

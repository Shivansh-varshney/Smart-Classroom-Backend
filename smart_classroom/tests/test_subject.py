import json
import hashlib
from smart_classroom.models import * 
from .BaseTestData import APITestData

class AdminAPITestCase(APITestData):

    def test_01_create_subject(self):
        """Test create subject"""

        response = self.client.post("/api/admin/subject/create/", {
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
                "course_id": self.course.id,            
                "teacher_id": self.teacher.id,            
                "name": "C++ Basics", 
        }, content_type='application/json')

        self.assertEqual(response.status_code, 403)
        self.assertIn("one or more fields missing", response.content.decode())
    
    def test_03_create_subject_without_teacher(self):
        """Test create subject with incomplete details"""

        response = self.client.post("/api/admin/subject/create/", {
                "course_id": self.course.id,        
                "name": "C++ Basics",
                "semester": 1, 
        }, content_type='application/json')

        self.assertEqual(response.status_code, 201)
        self.assertIn("Subject created successfully", response.content.decode())
    
    def test_04_create_subject_with_invalid_teacher(self):
        """Test create subject with incomplete details"""

        response = self.client.post("/api/admin/subject/create/", {
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
                "course_id": self.course.id,            
                "teacher_id": self.teacher.id,            
                "name": "C++ Basics",            
                "semester": 1,        
        }, content_type='application/json')

        self.assertEqual(response.status_code, 405)
        self.assertIn("Invalid request method", response.content.decode())

    def test_07_create_subject_with_invalid_admin(self):
        """Test create subject"""

        response = self.client.post('/api/user/login/', 
        data = {
            'email': 'testuser3@gmail.com',
            'password': 'password'
        }, content_type='application/json')

        self.token = f"Bearer {response.headers.get('ACCESS-TOKEN')}"
        if self.token:
            self.client.defaults['HTTP_AUTHORIZATION'] = self.token
            self.client.defaults['HTTP_USER_ID'] = str(self.user3.id)

        response = self.client.post("/api/admin/subject/create/", {
                "course_id": self.course.id,            
                "teacher_id": self.teacher.id,            
                "name": "C++ Basics",            
                "semester": 1,        
        }, content_type='application/json')

        self.assertEqual(response.status_code, 401)
        self.assertIn("unauthorized access", response.content.decode())
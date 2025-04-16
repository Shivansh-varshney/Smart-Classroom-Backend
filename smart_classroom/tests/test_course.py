import json
import hashlib
from .TestData import APITestData
from smart_classroom.models import EmailOTP

class CourseAPITests(APITestData):

    def test_01_create_course_with_all_valid_details(self):
        """Test create a course"""

        response = self.client.post("/api/admin/course/create/",{
            "degree_id": self.degree.id,
            "name": "Discipline Specific Core",
            "credits": 4
        }, content_type="application/json")

        self.assertEqual(response.status_code, 201)
        self.assertIn("Course created successfully", response.content.decode())
    
    def test_02_create_course_with_incomplete_details(self):
        """Test create a course with incomplete details"""

        response = self.client.post("/api/admin/course/create/",{
            "name": "Discipline Specific Core",
            "credits": 4
        }, content_type='application/json')
        
        self.assertEqual(response.status_code, 403)
        self.assertIn("one or more fields missing", response.content.decode())

    def test_03_create_course_with_invalid_request_method(self):
        """Test create course with invalid request method"""

        response = self.client.get("/api/admin/course/create/",{
            "name": "Discipline Specific Core",
            "credits": 4
        }, content_type='application/json')

        self.assertEqual(response.status_code, 405)
        self.assertIn("Invalid request method", response.content.decode())

    def test_04_create_course_with_invalid_degree(self):
        """Test create course with invalid degree"""

        response = self.client.post("/api/admin/course/create/",{
            "degree_id": 99,
            "name": "Discipline Specific Core",
            "credits": 4
        }, content_type="application/json")
        
        self.assertEqual(response.status_code, 404)
        self.assertIn("Degree does not exist", response.content.decode())

    def test_05_create_course_with_invalid_admin(self):
        """Test create a course with invalid admin"""
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

        response = self.client.post("/api/admin/course/create/",{
            "degree_id": self.degree.id,
            "name": "Discipline Specific Core",
              "credits": 4
        }, content_type="application/json")

        self.assertEqual(response.status_code, 401)
        self.assertIn("unauthorized access", response.content.decode())

    def test_06_create_course_for_unhandled_exceptions(self):
            """Test create a course"""

            response = self.client.post("/api/admin/course/create/",{
                """"degree_id": self.degree.id,
                "name": "Discipline Specific Core",
                "credits": 4"""
            }, content_type="application/json")

            self.assertEqual(response.status_code, 500)
            self.assertIn("Something went wrong", response.content.decode())

    def test_07_update_course_name(self):
        """Test update course name"""

        response = self.client.post("/api/admin/course/update/", {
            'course_id': self.course.id,
            'new_details': {
                'name': 'Skill Enhancement Course'
            }
        }, content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertIn("Course updated successfully", response.content.decode())
    
    def test_08_update_course_total_credits(self):
        """Test update course total credits"""

        response = self.client.post("/api/admin/course/update/", {
            'course_id': self.course.id,
            'new_details': {
                'total_credits': 10
            }
        }, content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertIn("Course updated successfully", response.content.decode())
    
    def test_09_update_course_invalid_field(self):
        """Test update course invalid field"""

        response = self.client.post("/api/admin/course/update/", {
            'course_id': self.course.id,
            'new_details': {
                'invalid field': 'invalid value'
            }
        }, content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertIn("invalid field is invalid field", response.content.decode())
    
    def test_10_update_course_with_missing_details(self):
        """Test update course with missing details"""

        response = self.client.post("/api/admin/course/update/", {
            'course_id': self.course.id
        }, content_type='application/json')

        self.assertEqual(response.status_code, 403)
        self.assertIn("one or more fields missing", response.content.decode())
    
    def test_11_update_course_with_invalid_request_method(self):
        """Test update course invalid request method"""

        response = self.client.get("/api/admin/course/update/", {
            'course_id': self.course.id,
            'new_details': {
                'total_credits': 10
            }
        }, content_type='application/json')

        self.assertEqual(response.status_code, 405)
        self.assertIn("Invalid request method", response.content.decode())
    
    def test_12_update_course_with_invalid_admin(self):
        """Test update course invalid request method"""
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

        response = self.client.post("/api/admin/course/update/", {
            'course_id': self.course.id,
            'new_details': {
                'total_credits': 10
            }
        }, content_type='application/json')

        self.assertEqual(response.status_code, 401)
        self.assertIn("unauthorized access", response.content.decode())
    
    def test_13_update_non_existent_course(self):
        """Test update non existent course"""

        response = self.client.post("/api/admin/course/update/", {
            'course_id': 99,
            'new_details': {
                'total_credits': 10
            }
        }, content_type='application/json')

        self.assertEqual(response.status_code, 404)
        self.assertIn("Course not found", response.content.decode()) 
      
    def test_14_update_course_degree(self):
        """Test update course degree"""

        response = self.client.post("/api/admin/course/update/", {
            'course_id': self.course.id,
            'new_details': {
                'degree': self.degree.id
            }
        }, content_type='application/json')

        self.assertEqual(response.status_code, 403)
        self.assertIn("Degree can not be changed", response.content.decode())

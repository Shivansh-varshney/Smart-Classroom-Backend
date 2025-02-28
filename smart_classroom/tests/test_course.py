import json
import hashlib
from django.urls import reverse
from smart_classroom.models import * 
from .BaseTestData import APITestData

class AdminAPITestCase(APITestData):

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

        response = self.client.post('/api/user/login/', 
        data = {
            'email': 'testuser3@gmail.com',
            'password': 'password'
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
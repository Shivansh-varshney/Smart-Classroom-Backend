import json
import hashlib
from smart_classroom.models import * 
from .BaseTestData import APITestData

class AdminAPITestCase(APITestData):

    def test_01_create_degree(self):
        """Test create a simple degree"""

        response = self.client.post('/api/admin/degree/create/',
        {
            "department_id": self.department.id,
            "title": "Bachelor Of Science",
            "branch": "Computer Science",
            "semesters": 8
        }, content_type="application/json")
        
        self.assertEqual(response.status_code, 201)
        self.assertIn("Degree created", response.content.decode())

    def test_02_create_degree_with_incomplete_details(self):
        """Test create degree with incomplete details"""

        response = self.client.post('/api/admin/degree/create/',
        {
            "title": "Bachelor Of Science",
            "branch": "Computer Science",
            "semesters": 8
        }, content_type="application/json")
        
        self.assertEqual(response.status_code, 403)
        self.assertIn("one or more fields missing", response.content.decode())

    def test_03_create_degree_with_invalid_request_method(self):
        """Test create degree with invalid request method"""

        response = self.client.get('/api/admin/degree/create/',
        {
            "title": "Bachelor Of Science",
            "branch": "Computer Science",
            "semesters": 8
        }, content_type="application/json")
        
        self.assertEqual(response.status_code, 405)
        self.assertIn("Invalid request method", response.content.decode())

    def test_04_create_degree_with_invalid_department(self):
        """Test create degree with invalid department"""

        response = self.client.post('/api/admin/degree/create/',
        {
            "department_id": 99,
            "title": "Bachelor Of Science",
            "branch": "Computer Science",
            "semesters": 8
        }, content_type="application/json")
        
        self.assertEqual(response.status_code, 404)
        self.assertIn("Department does not exist", response.content.decode())
    
    def test_05_create_degree_with_invalid_admin(self):
        """Test create a simple degree"""

        response = self.client.post('/api/user/login/', 
        data = {
            'email': 'testuser3@gmail.com',
            'password': 'password'
        }, content_type='application/json')

        self.token = f"Bearer {response.headers.get('ACCESS-TOKEN')}"
        if self.token:
            self.client.defaults['HTTP_AUTHORIZATION'] = self.token
            self.client.defaults['HTTP_USER_ID'] = str(self.user3.id)

        response = self.client.post('/api/admin/degree/create/',
        {
            "department_id": self.department.id,
            "title": "Bachelor Of Science",
            "branch": "Computer Science",
            "semesters": 8
        }, content_type="application/json")
        
        self.assertEqual(response.status_code, 401)
        self.assertIn("unauthorized access", response.content.decode())
        
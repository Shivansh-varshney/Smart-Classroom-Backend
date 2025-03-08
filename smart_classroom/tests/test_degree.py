import json
import hashlib
from smart_classroom.models import * 
from .TestData import APITestData

class DegreeAPITests(APITestData):

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
    
    def test_06_create_degree_for_unhandled_exceptions(self):
        """Test create a simple degree"""

        response = self.client.post('/api/admin/degree/create/',
        {
            """"department_id": self.department.id,
            "title": "Bachelor Of Science",
            "branch": [],
            "semesters": 8"""
        }, content_type="application/json")
        
        self.assertEqual(response.status_code, 400)
        self.assertIn("Something went wrong", response.content.decode())

    def test_07_update_degree_semesters(self):
        """Test update semesters of a degree"""

        response = self.client.post('/api/admin/degree/update/',
        {
            "degree_id": self.degree.id,
            "new_details": {
                'semesters': 6
            }
        }, content_type="application/json")
        
        self.assertEqual(response.status_code, 200)
        self.assertIn("Degree updated successfully", response.content.decode())
    
    def test_08_update_degree_title_and_branch(self):
        """Test update title and branch of a degree"""

        response = self.client.post('/api/admin/degree/update/',
        {
            "degree_id": self.degree.id,
            "new_details": {
                'title': 'Masters of Science',
                'branch': 'Artificial Intelligence'
            }
        }, content_type="application/json")
        
        self.assertEqual(response.status_code, 200)
        self.assertIn("Degree updated successfully", response.content.decode())
    
    def test_09_update_degree_department(self):
        """Test update department of a degree"""

        response = self.client.post('/api/admin/degree/update/',
        {
            "degree_id": self.degree.id,
            "new_details": {
                'department': 'Mathematics'
            }
        }, content_type="application/json")
        
        self.assertEqual(response.status_code, 403)
        self.assertIn("Department of a degree can not be changed", response.content.decode())
    
    def test_10_update_degree_with_missing_fields(self):
        """Test update degree with missing fields"""

        response = self.client.post('/api/admin/degree/update/',
        {
            "degree_id": self.degree.id,
        }, content_type="application/json")
        
        self.assertEqual(response.status_code, 403)
        self.assertIn("one or more fields missing", response.content.decode())
    
    def test_11_update_degree_with_invalid_fields(self):
        """Test update degree with invalid fields"""

        response = self.client.post('/api/admin/degree/update/',
        {
            "degree_id": self.degree.id,
            "new_details": {
                'invalid field': 'Invalid Value'
            }
        }, content_type="application/json")
        
        self.assertEqual(response.status_code, 400)
        self.assertIn("invalid field is invalid field", response.content.decode())
    
    def test_12_update_non_existent_degree(self):
        """Test update non existent degree"""

        response = self.client.post('/api/admin/degree/update/',
        {
            "degree_id": 99,
            "new_details": {
                'Invalid Field': 'Invalid Value'
            }
        }, content_type="application/json")
        
        self.assertEqual(response.status_code, 404)
        self.assertIn("Degree not found", response.content.decode())
    
    def test_13_update_degree_for_unhandled_exceptions(self):
        """Test update non existent degree"""

        response = self.client.post('/api/admin/degree/update/',
        {
            """"degree_id": 99,
            "new_details": {
                'Invalid Field': 'Invalid Value'
            }"""
        }, content_type="application/json")
        
        self.assertEqual(response.status_code, 400)
        self.assertIn("Something went wrong", response.content.decode())
    
    def test_14_update_degree_with_invalid_request_method(self):
        """Test update non existent degree"""

        response = self.client.get('/api/admin/degree/update/',
        {
            "degree_id": self.degree.id,
            "new_details": {
                'Invalid Field': 'Invalid Value'
            }
        }, content_type="application/json")
        
        self.assertEqual(response.status_code, 405)
        self.assertIn("Invalid request method", response.content.decode())
    
    def test_15_update_degree_with_invalid_admin(self):
        """Test update non existent degree"""

        response = self.client.post('/api/user/login/', 
        data = {
            'email': 'testuser3@gmail.com',
            'password': 'password'
        }, content_type='application/json')

        self.token = f"Bearer {response.headers.get('ACCESS-TOKEN')}"
        if self.token:
            self.client.defaults['HTTP_AUTHORIZATION'] = self.token
            self.client.defaults['HTTP_USER_ID'] = str(self.user3.id)

        response = self.client.post('/api/admin/degree/update/',
        {
            "degree_id": self.degree.id,
            "new_details": {
                'title': 'Masters of Science',
                'branch': 'Artificial Intelligence'
            }
        }, content_type="application/json")
        
        self.assertEqual(response.status_code, 401)
        self.assertIn("unauthorized access", response.content.decode())

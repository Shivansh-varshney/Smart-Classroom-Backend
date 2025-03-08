import json
import hashlib
from smart_classroom.models import *
from .TestData import APITestData

class DepartmentAPITests(APITestData):

    def test_01_create_department(self):
        """Test create department"""

        response = self.client.post('/api/admin/department/create/',
        {
            "organisation_id": self.organisation.id,
            "name": "Mathematics"
        }, content_type='application/json')

        self.assertEqual(response.status_code, 201)
        self.assertIn("Department created successfully", response.content.decode())
    
    def test_02_create_department_with_missing_details(self):
        """Test create department with missing details"""

        response = self.client.post('/api/admin/department/create/',
        {
            "name": "Mathematics Department"
        }, content_type='application/json')

        self.assertEqual(response.status_code, 403)
        self.assertIn("Organisation ID or name missing", response.content.decode())

    def test_03_create_department_with_invalid_organisation(self):
        """Test create department with invalid organisation"""

        response = self.client.post('/api/admin/department/create/',
        {
            "organisation_id": 99,
            "name": "Mathematics Department"
        }, content_type='application/json')

        self.assertEqual(response.status_code, 404)
        self.assertIn("Organisation not found", response.content.decode())
    
    def test_04_create_department_with_invalid_request_method(self):
        """Test create department with invalid request method"""

        response = self.client.get('/api/admin/department/create/',
        {
            "organisation_id": self.organisation.id,
            "name": "Mathematics Department"
        }, content_type='application/json')

        self.assertEqual(response.status_code, 405)
        self.assertIn("Invalid Request Method", response.content.decode())

    def test_05_get_department_with_valid_id(self):
        """Test get department when it exists"""

        response = self.client.post("/api/admin/department/", {
            "department_id": self.department.id
        }, content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertIn("Department found", response.content.decode())
    
    def test_06_get_department_with_invalid_id(self):
        """Test get department when it doesn't exist"""

        response = self.client.post("/api/admin/department/", {
            "department_id": 99
        }, content_type='application/json')

        self.assertEqual(response.status_code, 404)
        self.assertIn("Department not found", response.content.decode())
    
    def test_06_get_department_with_missing_details(self):
        """Test get department when it doesn't exist"""

        response = self.client.post("/api/admin/department/", {}, content_type='application/json')

        self.assertEqual(response.status_code, 403)
        self.assertIn("Department ID is required", response.content.decode())
    
    def test_07_get_department_with_invalid_request_method(self):
        """Test get department when it doesn't exist"""

        response = self.client.get("/api/admin/department/", {
            "department_id": self.department.id
        }, content_type='application/json')

        self.assertEqual(response.status_code, 405)
        self.assertIn("Invalid request method", response.content.decode())
    
    def test_08_create_department_with_invalid_admin(self):
        """Test create a simple degree with invalid admin"""

        response = self.client.post('/api/user/login/', 
        data = {
            'email': 'testuser3@gmail.com',
            'password': 'password'
        }, content_type='application/json')

        self.token = f"Bearer {response.headers.get('ACCESS-TOKEN')}"
        if self.token:
            self.client.defaults['HTTP_AUTHORIZATION'] = self.token
            self.client.defaults['HTTP_USER_ID'] = str(self.user3.id)

        response = self.client.post('/api/admin/department/create/',
        {
            "organisation_id": self.organisation.id,
            "name": "Mathematics"
        }, content_type='application/json')
        
        self.assertEqual(response.status_code, 401)
        self.assertIn("unauthorized access", response.content.decode())

    def test_09_get_department_with_invalid_admin(self):
        """Test get department with invalid admin"""

        response = self.client.post('/api/user/login/', 
        data = {
            'email': 'testuser3@gmail.com',
            'password': 'password'
        }, content_type='application/json')

        self.token = f"Bearer {response.headers.get('ACCESS-TOKEN')}"
        if self.token:
            self.client.defaults['HTTP_AUTHORIZATION'] = self.token
            self.client.defaults['HTTP_USER_ID'] = str(self.user3.id)

        response = self.client.post("/api/admin/department/", {
            "department_id": self.department.id
        }, content_type='application/json')

        self.assertEqual(response.status_code, 401)
        self.assertIn("unauthorized access", response.content.decode())

    def test_10_update_department(self):
        """Test update a department"""

        response = self.client.post("/api/admin/department/update/", {
            'department_id': self.department.id,
            'new_details': {
                'name': 'Information Technology'
            }
        }, content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertIn("Department updated successfully", response.content.decode())
    
    def test_11_update_department_with_invalid_request_method(self):
        """Test update a department with invalid request method"""

        response = self.client.get("/api/admin/department/update/", {
            'department_id': self.department.id,
            'new_details': {
                'name': 'Information Technology'
            }
        }, content_type='application/json')

        self.assertEqual(response.status_code, 405)
        self.assertIn("Invalid request method", response.content.decode())

    def test_12_update_organisation_of_department(self):
        """Test update organisation of a department"""

        response = self.client.post("/api/admin/department/update/", {
            'department_id': self.department.id,
            'new_details': {
                'organisation': 'Information Technology'
            }
        }, content_type='application/json')

        self.assertEqual(response.status_code, 403)
        self.assertIn("Organisation of department can not be changed", response.content.decode())
        
    def test_13_update_department_with_incomplete_details(self):
        """Test update a department with incomplete details"""

        response = self.client.post("/api/admin/department/update/", {
            'department_id': self.department.id
        }, content_type='application/json')

        self.assertEqual(response.status_code, 403)
        self.assertIn("one or more fields missing", response.content.decode())
    
    def test_14_update_department_with_invalid_admin(self):
        """Test update a department with invalid admin"""

        response = self.client.post('/api/user/login/', 
        data = {
            'email': 'testuser3@gmail.com',
            'password': 'password'
        }, content_type='application/json')

        self.token = f"Bearer {response.headers.get('ACCESS-TOKEN')}"
        if self.token:
            self.client.defaults['HTTP_AUTHORIZATION'] = self.token
            self.client.defaults['HTTP_USER_ID'] = str(self.user3.id)

        response = self.client.post("/api/admin/department/update/", {
            'department_id': self.department.id
        }, content_type='application/json')

        self.assertEqual(response.status_code, 401)
        self.assertIn("unauthorized access", response.content.decode())
    
    def test_15_update_department_for_unhandled_exceptions(self):
        """Test update a department with invalid admin"""

        response = self.client.post("/api/admin/department/update/", {
            """'department_id': self.department.id"""
        }, content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertIn("Something went wrong", response.content.decode())

    def test_16_create_department_for_unhandled_exceptions(self):
        """Test create department"""

        response = self.client.post('/api/admin/department/create/',
        {
            """organisation_id": self.organisation.id,
            "name": "Mathematics"""
        }, content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertIn("Something went wrong", response.content.decode())

    def test_17_get_department_for_unhandled_exceptions(self):
        """Test get department when it exists"""

        response = self.client.post("/api/admin/department/", {
            """"department_id": self.department.id"""
        }, content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertIn("Something went wrong", response.content.decode())
    
    def test_18_update_organisation_of_department_for_invalid_department(self):
        """Test update organisation of a department"""

        response = self.client.post("/api/admin/department/update/", {
            'department_id': 99,
            'new_details': {
                'organisation': 'Information Technology'
            }
        }, content_type='application/json')

        self.assertEqual(response.status_code, 404)
        self.assertIn("Department not found", response.content.decode())

    def test_19_update_department_with_invalid_field(self):
        """Test update a department"""

        response = self.client.post("/api/admin/department/update/", {
            'department_id': self.department.id,
            'new_details': {
                'invalid field': 'Invalid Value'
            }
        }, content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertIn("invalid field is invalid field", response.content.decode())

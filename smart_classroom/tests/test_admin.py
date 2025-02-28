import json
import hashlib
from smart_classroom.models import * 
from .BaseTestData import APITestData

class AdminAPITestCase(APITestData):

    def test_01_admin_signup(self):
        """Test admin signup endpoint."""
        response = self.client.post('/api/admin/signup/', 
        data = {
            'first_name':'first_name', 
            'last_name':'last_name', 
            'phone':'+911122334455',
            'email': 'newadmin@example.com',
            'password': str(hashlib.sha256('securepass'.encode()).hexdigest())
        }, content_type='application/json')
        self.assertEqual(response.status_code, 201)
    
    def test_02_admin_signup_using_existing_email(self):
        """Test to see that same email doesn't create two admin accounts"""

        response = self.client.post('/api/admin/signup/',
        data = {
            'first_name':'first_name', 
            'last_name':'last_name', 
            'phone':'+911122334455',
            'email': 'testuser@gmail.com',
            'password': str(hashlib.sha256('securepass'.encode()).hexdigest())
        }, content_type='application/json'
        )

        self.assertEqual(response.status_code, 403)
        self.assertIn('Email already in use', response.content.decode())
    
    def test_03_admin_signup_with_missing_details(self):
        """Test to see admin isn't created with missing details"""

        response = self.client.post('/api/admin/signup/',
        data = {
            'first_name':'first_name', 
            'last_name':'last_name', 
            'phone':'+911122334455',
            'password': 'securepass'
        }, content_type='application/json'
        )

        self.assertEqual(response.status_code, 403)
        self.assertIn('One or more details missing', response.content.decode())

    def test_04_admin_login(self):
        """Test user login endpoint."""
        response = self.client.post('/api/user/login/', 
        data = {
            'email': 'testuser@gmail.com',
            'password': 'password'
        }, content_type='application/json')
        self.token = f"Bearer {response.headers.get('ACCESS-TOKEN')}"
        self.assertEqual(response.status_code, 200)
    
    def test_05_admin_login_with_missing_details(self):
        """Test user login endpoint."""
        response = self.client.post('/api/user/login/', 
        data = {
            'email': 'testuser@gmail.com'
        }, content_type='application/json')
        self.assertEqual(response.status_code, 403)
        self.assertIn('Credentials incomplete', response.content.decode())

    def test_06_admin_login_with_wrong_email(self):
        """Test user login endpoint with wrong email"""
        response = self.client.post('/api/user/login/', 
        data = {
            'email': 'wrongtestuser@gmail.com',
            'password': 'wrongpassword'
        }, content_type='application/json')
        self.assertEqual(response.status_code, 404)
        self.assertIn('Email not found', response.content.decode())

    def test_07_admin_login_with_wrong_password(self):
        """Test user login endpoint with wrong password"""
        response = self.client.post('/api/user/login/', 
        data = {
            'email': 'testuser@gmail.com',
            'password': 'wrongpassword'
        }, content_type='application/json')
        self.assertEqual(response.status_code, 403)
        self.assertIn('Wrong password', response.content.decode())
    
    def test_08_admin_login_with_invalid_request_method(self):
        """Test user login endpoint with wrong password"""
        response = self.client.get('/api/user/login/', 
        data = {
            'email': 'testuser@gmail.com',
            'password': 'password'
        }, content_type='application/json')
        self.assertEqual(response.status_code, 405)
        self.assertIn('Invalid request method', response.content.decode())

    def test_09_admin_signup_with_invalid_request_method(self):
        """Test admin signup endpoint."""
        response = self.client.get('/api/admin/signup/', 
        data = {
            'first_name':'first_name', 
            'last_name':'last_name', 
            'phone':'+911122334455',
            'email': 'newadmin@example.com',
            'password': str(hashlib.sha256('securepass'.encode()).hexdigest())
        }, content_type='application/json')
        self.assertEqual(response.status_code, 405)
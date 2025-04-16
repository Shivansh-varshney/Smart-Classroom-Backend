import json
import hashlib
from .TestData import APITestData
from smart_classroom.models import EmailOTP

class AdminAPITests(APITestData):

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

    def test_10_create_another_admin(self):
        """Test create another admin for same organisation as admmin"""
        response = self.client.post('/api/admin/other_admin/create/', 
        data = {
            'first_name':'first_name', 
            'last_name':'last_name', 
            'phone':'+911122334455',
            'email': 'newadmin@example.com',
            'password': str(hashlib.sha256('securepass'.encode()).hexdigest())
        }, content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertIn("admin added successfully", response.content.decode())
    
    def test_11_create_another_admin_with_incomplete_details(self):
        """Test create another admin for same organisation as admmin with incomplete details"""
        response = self.client.post('/api/admin/other_admin/create/', 
        data = {
            'first_name':'first_name', 
            'last_name':'last_name',
            'email': 'newadmin@example.com',
            'password': str(hashlib.sha256('securepass'.encode()).hexdigest())
        }, content_type='application/json')
        self.assertEqual(response.status_code, 403)
        self.assertIn("one or more fields missing", response.content.decode())
    
    def test_12_create_another_admin_with_invalid_request_method(self):
        """Test create another admin for same organisation as admmin with incomplete details"""
        response = self.client.get('/api/admin/other_admin/create/', 
        data = {
            'first_name':'first_name', 
            'last_name':'last_name',
            'email': 'newadmin@example.com',
            'password': str(hashlib.sha256('securepass'.encode()).hexdigest())
        }, content_type='application/json')
        self.assertEqual(response.status_code, 405)
        self.assertIn("Invalid request method", response.content.decode())
    
    def test_13_create_another_admin_using_existing_admin_details(self):
        """Test create another admin for same organisation as admmin with incomplete details"""
        response = self.client.post('/api/admin/other_admin/create/', 
        data = {
            'first_name':'first_name', 
            'last_name':'last_name',
            'phone':'+911122334455',
            'email': 'testuser@gmail.com',
            'password': str(hashlib.sha256('securepass'.encode()).hexdigest())
        }, content_type='application/json')
        self.assertEqual(response.status_code, 401)
        self.assertIn("Admin already exists", response.content.decode())

    def test_14_create_another_admin_with_invalid_admin(self):
        """Test create another admin for same organisation as admmin"""

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

        response = self.client.post('/api/admin/other_admin/create/', 
        data = {
            'first_name':'first_name', 
            'last_name':'last_name', 
            'phone':'+911122334455',
            'email': 'newadmin@example.com',
            'password': str(hashlib.sha256('securepass'.encode()).hexdigest())
        }, content_type='application/json')
        self.assertEqual(response.status_code, 401)
        self.assertIn("unauthorized access", response.content.decode())
    
    def test_15_create_another_admin_for_unhandled_exceptions(self):
        """Test create another admin for same organisation as admmin"""

        response = self.client.post('/api/admin/other_admin/create/', 
        data = {
            """'first_name':'first_name', 
            'last_name':'last_name', 
            'phone':'+911122334455',
            'email': 'newadmin@example.com',
            'password': str(hashlib.sha256('securepass'.encode()).hexdigest())"""
        }, content_type='application/json')
        self.assertEqual(response.status_code, 500)
        self.assertIn("Something went wrong", response.content.decode())    
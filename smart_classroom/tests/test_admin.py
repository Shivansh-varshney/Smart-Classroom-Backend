import json
import hashlib
from smart_classroom.models import * 
from django.urls import reverse
from django.test import TestCase, Client

class AdminAPITestCase(TestCase):

    @classmethod
    def setUpTestData(cls):

        # this is user for all normal tests
        cls.user = User.objects.create(
        username='testuser', 
        first_name='first_name', 
        last_name='last_name', 
        phone='phone', 
        email='testuser@gmail.com', 
        role='admin', 
        password=hashlib.sha256('password'.encode()).hexdigest())

    def setUp(self):

        self.client = Client()
        response = self.client.post('/api/user/login/', 
        data = {
            'email': 'testuser@gmail.com',
            'password': 'password'
        }, content_type='application/json')

        self.token = f"Bearer {response.headers.get('AUTHORIZATION')}"
        if self.token:
            self.client.defaults['HTTP_AUTHORIZATION'] = self.token
            self.client.defaults['HTTP_USER_ID'] = str(self.user.id)

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
        self.token = f"Bearer {response.headers.get('AUTHORIZATION')}"
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

import json
import hashlib
from smart_classroom.models import * 
from django.urls import reverse
from django.test import TestCase, Client

class OrganisationAPITestCase(TestCase):

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

        # this second user is for test_10_create_second_organisation_for_an_admin
        cls.user2 = User.objects.create(
        username='testuser2', 
        first_name='first_name2', 
        last_name='last_name2', 
        phone='phone2', 
        email='testuser2@gmail.com', 
        role='admin', 
        password=hashlib.sha256('password'.encode()).hexdigest())

        # create organisation for the user2
        cls.organisation = Organisation.objects.create(
            user=cls.user2,
            name='First Organisation',
            orgType='Private School'
        )

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
        self.assertEqual(response.status_code, 200)
    
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

        self.assertEqual(response.status_code, 400)
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

        self.assertEqual(response.status_code, 400)
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
        self.assertEqual(response.status_code, 400)
        self.assertIn('Credentials incomplete', response.content.decode())

    def test_06_admin_login_with_wrong_email(self):
        """Test user login endpoint with wrong email"""
        response = self.client.post('/api/user/login/', 
        data = {
            'email': 'wrongtestuser@gmail.com',
            'password': 'wrongpassword'
        }, content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('Email not found', response.content.decode())

    def test_07_admin_login_with_wrong_password(self):
        """Test user login endpoint with wrong password"""
        response = self.client.post('/api/user/login/', 
        data = {
            'email': 'testuser@gmail.com',
            'password': 'wrongpassword'
        }, content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('Wrong password', response.content.decode())

    def test_08_create_new_organisation_with_incomplete_details(self):
        """Test creating a new organisation for a user with incomplete details"""
        response = self.client.post('/api/admin/organisation/create/', 
        data = {
            'name': 'New Org',
        },
        content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('Name and type are required', response.content.decode())

    def test_09_create_first_organisation_for_an_admin(self):
        """Test creating a new organisation for a user when they have no organisation"""
        response = self.client.post('/api/admin/organisation/create/', 
        data = {
            'name': 'New Org',
            'type': 'College',
            'board': 'State Board'
        },
        content_type='application/json')
        self.assertEqual(response.status_code, 201)
    
    def test_10_create_second_organisation_for_an_admin(self):
        """Test creating a new organisation for a user when they already have an organisation"""

        # setting up auth headers
        self.client = Client()
        response = self.client.post('/api/user/login/', 
        data = {
            'email': 'testuser2@gmail.com',
            'password': 'password'
        }, content_type='application/json')

        self.token = f"Bearer {response.headers.get('AUTHORIZATION')}"
        if self.token:
            self.client.defaults['HTTP_AUTHORIZATION'] = self.token
            self.client.defaults['HTTP_USER_ID'] = str(self.user2.id)

        # sending request to create second organisation for the user2
        response = self.client.post('/api/admin/organisation/create/', 
        data = {
            'name': 'Second Organisation',
            'type': 'Private School',
            'board': 'CBSE: Central Board of Secondary Education'
        },
        content_type='application/json')
        self.assertEqual(response.status_code, 401)
        self.assertIn('User already has an organisation.', response.content.decode())

    def test_11_get_organisation(self):
        """Test fetching organisation details."""
        
        response = self.client.get('/api/admin/organisation/'
        ,
        content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('organisation', response.content.decode())
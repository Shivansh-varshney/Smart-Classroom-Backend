import json
import hashlib
from smart_classroom.models import * 
from django.urls import reverse
from django.test import TestCase, Client

class OrganisationAPITestCase(TestCase):

    @classmethod
    def setUpTestData(cls):

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

    def test_admin_signup(self):
        """Test admin signup endpoint."""
        response = self.client.post('/api/admin/signup/', 
        data = {
            'first_name':'first_name', 
            'last_name':'last_name', 
            'phone':'+911122334455',
            'email': 'newadmin@example.com',
            'password': 'securepass'
        }, content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_admin_login(self):
        """Test user login endpoint."""
        response = self.client.post('/api/user/login/', 
        data = {
            'email': 'testuser@gmail.com',
            'password': 'password'
        }, content_type='application/json')
        self.token = f"Bearer {response.headers.get('AUTHORIZATION')}"
        self.assertEqual(response.status_code, 200)

    def test_create_organisation(self):
        """Test creating a new organisation."""
        response = self.client.post('/api/admin/organisation/create/', 
        data = {
            'name': 'New Org',
            'type': 'College',
            'board': 'State Board'
        },
        content_type='application/json')
        self.assertEqual(response.status_code, 201)
    
    def test_get_organisation(self):
        """Test fetching organisation details."""
        
        response = self.client.get('/api/admin/organisation/'
        ,
        content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('organisation', response.content.decode())
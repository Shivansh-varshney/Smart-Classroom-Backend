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

    def test_1_create_new_organisation_with_incomplete_details(self):
        """Test creating a new organisation for a user with incomplete details"""
        response = self.client.post('/api/admin/organisation/create/', 
        data = {
            'name': 'New Org',
        },
        content_type='application/json')
        self.assertEqual(response.status_code, 403)
        self.assertIn('Name and type are required', response.content.decode())

    def test_2_create_first_organisation_for_an_admin(self):
        """Test creating a new organisation for a user when they have no organisation"""
        response = self.client.post('/api/admin/organisation/create/', 
        data = {
            'name': 'New Org',
            'type': 'College',
            'board': 'State Board'
        },
        content_type='application/json')
        self.assertEqual(response.status_code, 201)
    
    def test_3_create_second_organisation_for_an_admin(self):
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
        self.assertEqual(response.status_code, 403)
        self.assertIn('User already has an organisation.', response.content.decode())

    def test_4_get_organisation(self):
        """Test fetching organisation details."""
        
        response = self.client.post('/api/admin/organisation/'
        ,
        content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('organisation', response.content.decode())
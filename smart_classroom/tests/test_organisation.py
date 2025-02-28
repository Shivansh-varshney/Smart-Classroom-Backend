import json
import hashlib
from django.urls import reverse
from .BaseTestData import APITestData
from smart_classroom.models import *

class OrganisationAPITestCase(APITestData):

    def test_01_create_new_organisation_with_incomplete_details(self):
        """Test creating a new organisation for a user with incomplete details"""

        # user2 doesn't has an organisation
        response = self.client.post('/api/user/login/', 
        data = {
            'email': 'testuser2@gmail.com',
            'password': 'password'
        }, content_type='application/json')

        self.token = f"Bearer {response.headers.get('ACCESS-TOKEN')}"
        if self.token:
            self.client.defaults['HTTP_AUTHORIZATION'] = self.token
            self.client.defaults['HTTP_USER_ID'] = str(self.user2.id)

        response = self.client.post('/api/admin/organisation/create/', 
        data = {
            'name': 'New Org',
        },
        content_type='application/json')
        self.assertEqual(response.status_code, 403)
        self.assertIn('Name and type are required', response.content.decode())

    def test_02_create_first_organisation_for_an_admin(self):
        """Test creating a new organisation for a user when they have no organisation"""

        # user2 doesn't has an organisation
        response = self.client.post('/api/user/login/', 
        data = {
            'email': 'testuser2@gmail.com',
            'password': 'password'
        }, content_type='application/json')

        self.token = f"Bearer {response.headers.get('ACCESS-TOKEN')}"
        if self.token:
            self.client.defaults['HTTP_AUTHORIZATION'] = self.token
            self.client.defaults['HTTP_USER_ID'] = str(self.user2.id)

        response = self.client.post('/api/admin/organisation/create/', 
        data = {
            'name': 'New Org',
            'type': 'College',
            'board': 'State Board'
        },
        content_type='application/json')
        self.assertEqual(response.status_code, 201)
    
    def test_03_create_first_organisation_for_an_admin_with_invalid_request_method(self):
        """Test creating a new organisation for a user when they have no organisation with invalid request method"""
        
        response = self.client.get('/api/admin/organisation/create/', 
        data = {
            'name': 'New Org',
            'type': 'College',
            'board': 'State Board'
        },
        content_type='application/json')
        self.assertEqual(response.status_code, 405)
        self.assertIn("Invalid request method", response.content.decode())
    
    def test_04_create_second_organisation_for_an_admin(self):
        """Test creating a new organisation for a user when they already have an organisation"""

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

    def test_05_get_organisation_when_user_has_organisation(self):
        """Test fetching organisation details."""
        
        response = self.client.post('/api/admin/organisation/'
        ,
        content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('Organisation found', response.content.decode())
    
    def test_06_get_organisation_when_user_has_no_organisation(self):
        """Test fetching organisation details."""

        # user2 doesn't has an organisation
        response = self.client.post('/api/user/login/', 
        data = {
            'email': 'testuser2@gmail.com',
            'password': 'password'
        }, content_type='application/json')

        self.token = f"Bearer {response.headers.get('ACCESS-TOKEN')}"
        if self.token:
            self.client.defaults['HTTP_AUTHORIZATION'] = self.token
            self.client.defaults['HTTP_USER_ID'] = str(self.user2.id)

        response = self.client.post('/api/admin/organisation/'
        ,
        content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn("No organisation", response.content.decode())
    
    def test_07_get_organisation_with_invalid_request_method(self):
        """Test fetching organisation details."""
        
        # for request method it does not matter whether the user has an organisation
        response = self.client.get('/api/admin/organisation/'
        ,
        content_type='application/json')
        self.assertEqual(response.status_code, 405)
        self.assertIn("Invalid request method", response.content.decode())

    def test_08_create_first_organisation_for_an_invalid_admin(self):
        """Test creating a new organisation for a user when they have no organisation"""

        response = self.client.post('/api/user/login/', 
        data = {
            'email': 'testuser3@gmail.com',
            'password': 'password'
        }, content_type='application/json')

        self.token = f"Bearer {response.headers.get('ACCESS-TOKEN')}"
        if self.token:
            self.client.defaults['HTTP_AUTHORIZATION'] = self.token
            self.client.defaults['HTTP_USER_ID'] = str(self.user3.id)

        response = self.client.post('/api/admin/organisation/create/', 
        data = {
            'name': 'New Org',
            'type': 'College',
            'board': 'State Board'
        },
        content_type='application/json')

        self.assertEqual(response.status_code, 401)
        self.assertIn('unauthorized access', response.content.decode())

    def test_09_get_organisation_with_invalid_admin(self):
        """Test fetching organisation with invalid admin"""

        response = self.client.post('/api/user/login/', 
        data = {
            'email': 'testuser3@gmail.com',
            'password': 'password'
        }, content_type='application/json')

        self.token = f"Bearer {response.headers.get('ACCESS-TOKEN')}"
        if self.token:
            self.client.defaults['HTTP_AUTHORIZATION'] = self.token
            self.client.defaults['HTTP_USER_ID'] = str(self.user3.id)
        
        response = self.client.post('/api/admin/organisation/'
        ,
        content_type='application/json')
        
        self.assertEqual(response.status_code, 401)
        self.assertIn('unauthorized access', response.content.decode())
    
    def test_10_get_organisation_with_invalid_user(self):
        """Test fetching organisation with invalid admin"""

        self.client.defaults['HTTP_USER_ID'] = 99
        response = self.client.post('/api/admin/organisation/'
        ,
        content_type='application/json')
        
        self.assertEqual(response.status_code, 401)
        self.assertIn('unauthorized access', response.content.decode())
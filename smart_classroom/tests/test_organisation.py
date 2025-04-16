import json
import hashlib
from .TestData import APITestData
from smart_classroom.models import EmailOTP

class OrganisationAPITests(APITestData):

    def test_01_create_new_organisation_with_incomplete_details(self):
        """Test creating a new organisation for a user with incomplete details"""

        # user2 doesn't has an organisation
        self.otp = EmailOTP.objects.create(email='testuser2@gmail.com', otp=hashlib.sha256('000111'.encode()).hexdigest())

        response = self.client.post('/api/user/verify-otp/', 
        data = {
            'email': 'testuser2@gmail.com',
            'otp': '000111'
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
        self.otp = EmailOTP.objects.create(email='testuser2@gmail.com', otp=hashlib.sha256('000111'.encode()).hexdigest())

        response = self.client.post('/api/user/verify-otp/', 
        data = {
            'email': 'testuser2@gmail.com',
            'otp': '000111'
        }, content_type='application/json')

        self.token = f"Bearer {response.headers.get('ACCESS-TOKEN')}"
        if self.token:
            self.client.defaults['HTTP_AUTHORIZATION'] = self.token
            self.client.defaults['HTTP_USER_ID'] = str(self.user2.id)


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
        self.otp = EmailOTP.objects.create(email='testuser2@gmail.com', otp=hashlib.sha256('000111'.encode()).hexdigest())

        response = self.client.post('/api/user/verify-otp/', 
        data = {
            'email': 'testuser2@gmail.com',
            'otp': '000111'
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

    def test_11_updating_an_organistaion_with_missing_details(self):
        """Test updating organisation with missing details"""

        response = self.client.post('/api/admin/organisation/update/'
        ,
        content_type='application/json')
        
        self.assertEqual(response.status_code, 403)
        self.assertIn('new_details field missing', response.content.decode())
    
    def test_12_updating_an_organistaion_with_invalid_request_method(self):
        """Test updating organisation with invalid request method"""

        response = self.client.get('/api/admin/organisation/update/'
        ,
        content_type='application/json')
        
        self.assertEqual(response.status_code, 405)
        self.assertIn('Invalid request method', response.content.decode())

    def test_13_update_name_of_an_existing_organisation(self):
        """Test update name of an existing organisation"""

        response = self.client.post('/api/admin/organisation/update/'
        ,{
            'new_details': {
                'name': 'Updated Name'
            }
        },
        content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('Organisation updated successfully', response.content.decode())
        
    def test_14_update_board_and_type_of_an_existing_organisation(self):
        """Test update name of an existing organisation"""

        response = self.client.post('/api/admin/organisation/update/'
        ,{
            'new_details': {
                'orgType': 'Updated Type',
                'board': 'Updated board'
            }
        },
        content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('Organisation updated successfully', response.content.decode())
    
    def test_15_update_an_existing_organisation_using_invalid_input(self):
        """Test update name of an existing organisation"""

        response = self.client.post('/api/admin/organisation/update/'
        ,{
            'new_details': ['invalid input']
        },
        content_type='application/json')
        
        self.assertEqual(response.status_code, 500)
        self.assertIn('Something went wrong', response.content.decode())
    
    def test_16_update_name_of_an_existing_organisation_with_invalid_admin(self):
        """Test update name of an existing organisation with invalid admin"""

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

        response = self.client.post('/api/admin/organisation/update/'
        ,{
            'new_details': {
                'name': 'Updated Name'
            }
        },
        content_type='application/json')
        
        self.assertEqual(response.status_code, 401)
        self.assertIn('unauthorized access', response.content.decode())
    
    def test_17_update_organisation_for_unhandled_exceptions(self):
        """Test update organisation for unhandled exceptions"""

        response = self.client.post('/api/admin/organisation/update/'
        ,{
            """'new_details': {
                'name': 'Updated Name'
            }"""
        },
        content_type='application/json')
        
        self.assertEqual(response.status_code, 500)
        self.assertIn('Something went wrong', response.content.decode())

    def test_18_create_first_organisation_for_an_admin_for_unhandled_exceptions(self):
        """Test creating a new organisation for an admin for unhandled exceptions"""

        # user2 doesn't has an organisation
        self.otp = EmailOTP.objects.create(email='testuser2@gmail.com', otp=hashlib.sha256('000111'.encode()).hexdigest())

        response = self.client.post('/api/user/verify-otp/', 
        data = {
            'email': 'testuser2@gmail.com',
            'otp': '000111'
        }, content_type='application/json')

        self.token = f"Bearer {response.headers.get('ACCESS-TOKEN')}"
        if self.token:
            self.client.defaults['HTTP_AUTHORIZATION'] = self.token
            self.client.defaults['HTTP_USER_ID'] = str(self.user2.id)

        response = self.client.post('/api/admin/organisation/create/', 
        {
            """'name': 'New Org',
            'type': 'College',
            'board': 'State Board',"""
        },
        content_type='application/json')
        self.assertEqual(response.status_code, 500)

    def test_19_update_invalid_field_of_an_existing_organisation(self):
        """Test update invalid field of an existing organisation"""

        response = self.client.post('/api/admin/organisation/update/'
        ,{
            'new_details': {
                'invalid field': 'Invalid Value'
            }
        },
        content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        self.assertIn('invalid field is invalid field', response.content.decode())
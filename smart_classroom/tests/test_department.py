import json
import hashlib
from smart_classroom.models import * 
from django.urls import reverse
from django.test import TestCase, Client

class DepartmentAPITestCase(TestCase):

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

        # create organisation for the user
        cls.organisation = Organisation.objects.create(
            user=cls.user,
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

    def test_1_create_department(self):
        """Test create department"""

        response = self.client.post('/api/admin/department/create/',
        {
            "organisation_id": self.organisation.id,
            "name": "Mathematics"
        }, content_type='application/json')

        self.assertEqual(response.status_code, 201)
        self.assertIn("Department created successfully", response.content.decode())
    
    def test_2_create_department_with_missing_details(self):
        """Test create department with missing details"""

        response = self.client.post('/api/admin/department/create/',
        {
            "name": "Mathematics Department"
        }, content_type='application/json')

        self.assertEqual(response.status_code, 403)
        self.assertIn("Organisation ID or name missing", response.content.decode())

    def test_3_create_department_with_invalid_organisation(self):
        """Test create department with invalid organisation"""

        response = self.client.post('/api/admin/department/create/',
        {
            "organisation_id": 99,
            "name": "Mathematics Department"
        }, content_type='application/json')

        self.assertEqual(response.status_code, 404)
        self.assertIn("Organisation not found", response.content.decode())
    
    def test_4_create_department_with_invalid_request_method(self):
        """Test create department with invalid request method"""

        response = self.client.get('/api/admin/department/create/',
        {
            "organisation_id": self.organisation.id,
            "name": "Mathematics Department"
        }, content_type='application/json')

        self.assertEqual(response.status_code, 405)
        self.assertIn("Invalid Request Method", response.content.decode())

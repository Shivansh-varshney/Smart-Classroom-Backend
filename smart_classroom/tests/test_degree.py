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

        # create organisation for the user
        cls.organisation = Organisation.objects.create(
            user=cls.user,
            name='First Organisation',
            orgType='Private School'
        )

        # create department for the organisation
        cls.department = Department.objects.create(
            organisation=cls.organisation,
            name="Computer Science"
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

    def test_01_create_degree(self):
        """Test create a simple degree"""

        response = self.client.post('/api/admin/degree/create/',
        {
            "department_id": self.department.id,
            "title": "Bachelor Of Science",
            "branch": "Computer Science",
            "semesters": 8
        }, content_type="application/json")
        
        self.assertEqual(response.status_code, 201)
        self.assertIn("Degree created", response.content.decode())

    def test_02_create_degree_with_incomplete_details(self):
        """Test create degree with incomplete details"""

        response = self.client.post('/api/admin/degree/create/',
        {
            "title": "Bachelor Of Science",
            "branch": "Computer Science",
            "semesters": 8
        }, content_type="application/json")
        
        self.assertEqual(response.status_code, 403)
        self.assertIn("one or more fields missing", response.content.decode())

    def test_03_create_degree_with_invalid_request_method(self):
        """Test create degree with invalid request method"""

        response = self.client.get('/api/admin/degree/create/',
        {
            "title": "Bachelor Of Science",
            "branch": "Computer Science",
            "semesters": 8
        }, content_type="application/json")
        
        self.assertEqual(response.status_code, 405)
        self.assertIn("Invalid request method", response.content.decode())

    def test_04_create_degree_with_invalid_department(self):
        """Test create degree with invalid department"""

        response = self.client.post('/api/admin/degree/create/',
        {
            "department_id": 99,
            "title": "Bachelor Of Science",
            "branch": "Computer Science",
            "semesters": 8
        }, content_type="application/json")
        
        self.assertEqual(response.status_code, 404)
        self.assertIn("Department does not exist", response.content.decode())
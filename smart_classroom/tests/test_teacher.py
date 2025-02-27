import json
import hashlib
from smart_classroom.models import * 
from django.urls import reverse
from django.test import TestCase, Client
from django.core.files.uploadedfile import SimpleUploadedFile

class AdminAPITestCase(TestCase):

    @classmethod
    def setUpTestData(cls):

        # user for admin role
        cls.user = User.objects.create(
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

    def test_01_create_teacher(self):
        """Test create a teacher"""

        with open("/home/shivansh/Desktop/all_codes/smart_classroom/smart_classroom_backend/media/teachers/Untitled.jpeg", "rb") as img_file:
            uploaded_image = SimpleUploadedFile(
                "image.jpg", img_file.read() , content_type='image/jpg'
            )

        response = self.client.post("/api/admin/teacher/create/", {
            "department_id": self.department.id,
            "first_name": "Some Name",
            "last_name": "for a teacher",
            "phone": "here phone",
            "email": "teacher@school.com",
            "image": uploaded_image,
            "salary": 120000,
            "password": "securepassword",
        }, format='multipart')

        self.assertEqual(response.status_code, 201)
        self.assertIn("Teaher created successfully", response.content.decode())
    
    def test_02_create_teacher_with_missing_fields(self):
        """Test create a teacher with missing fields"""

        response = self.client.post("/api/admin/teacher/create/", {
            "department_id": self.department.id,
            "first_name": "Some Name",
            "last_name": "for a teacher",
            "phone": "here phone",
            "email": "teacher@school.com",
        }, format='multipart')

        self.assertEqual(response.status_code, 403)
        self.assertIn("One or more fields missing", response.content.decode())

    def test_03_create_teacher_with_invalid_department(self):
        """Test create a teacher with invalid department"""

        with open("/home/shivansh/Desktop/all_codes/smart_classroom/smart_classroom_backend/media/teachers/Untitled.jpeg", "rb") as img_file:
            uploaded_image = SimpleUploadedFile(
                "image.jpg", img_file.read() , content_type='image/jpg'
            )

        response = self.client.post("/api/admin/teacher/create/", {
            "department_id": 99,
            "first_name": "Some Name",
            "last_name": "for a teacher",
            "phone": "here phone",
            "email": "teacher@school.com",
            "image": uploaded_image,
            "salary": 120000,
            "password": "securepassword",
        }, format='multipart')

        self.assertEqual(response.status_code, 404)
        self.assertIn("Department not found", response.content.decode())
    
    def test_04_create_teacher_with_invalid_request_method(self):
        """Test create a teacher with invalid request method"""

        with open("/home/shivansh/Desktop/all_codes/smart_classroom/smart_classroom_backend/media/teachers/Untitled.jpeg", "rb") as img_file:
            uploaded_image = SimpleUploadedFile(
                "image.jpg", img_file.read() , content_type='image/jpg'
            )

        response = self.client.get("/api/admin/teacher/create/", {
            "department_id": 99,
            "first_name": "Some Name",
            "last_name": "for a teacher",
            "phone": "here phone",
            "email": "teacher@school.com",
            "image": uploaded_image,
            "salary": 120000,
            "password": "securepassword",
        }, format='multipart')

        self.assertEqual(response.status_code, 405)
        self.assertIn("Invalid request method", response.content.decode())
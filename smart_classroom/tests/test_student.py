import json
import hashlib
from smart_classroom.models import * 
from django.urls import reverse
from django.test import TestCase, Client
from django.core.files.uploadedfile import SimpleUploadedFile

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

        # create degree
        cls.degree = Degree.objects.create(
            department=cls.department,
            title="Bachelor Of Science",
            branch="Computer Science",
            semesters=8
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

    def test_01_create_student(self):
        """Test create a student"""

        with open("/home/shivansh/Desktop/all_codes/smart_classroom/smart_classroom_backend/media/teachers/Untitled.jpeg", "rb") as img_file:
            uploaded_image = SimpleUploadedFile(
                "image.jpg", img_file.read() , content_type='image/jpg'
            )

        response = self.client.post("/api/admin/student/create/", {
                "degree_id": self.degree.id,
                "first_name": "New",
                "last_name": "Student",
                "phone": "phone",
                "email": "studentemail@school,com",
                "image": uploaded_image,
                "password": "securepassword",
                "semester": 1,
                "roll_number": 230359,
                "category": "General",
                "father_name": "Father Name",
                "mother_name": "Mother Name",
                "father_occupation": "Self Employed",
                "mother_occupation": "House Wife",
                "parent_phone": "newphone",
                "parent_email": "parentemail@school.com",
        }, format='multipart')

        self.assertEqual(response.status_code, 201)
        self.assertIn("Student created successfully", response.content.decode())
    
    def test_02_create_student_with_incomplete_details(self):
        """Test create a student with incomplete details"""

        response = self.client.post("/api/admin/student/create/", {
                "degree_id": self.degree.id,
                "first_name": "New",
                "last_name": "Student",
                "phone": "phone",
                "semester": 1,
                "roll_number": 230359,
                "category": "General",
                "father_name": "Father Name",
                "mother_name": "Mother Name",
                "father_occupation": "Self Employed",
                "mother_occupation": "House Wife",
                "parent_phone": "newphone",
                "parent_email": "parentemail@school.com",
        }, format='multipart')

        self.assertEqual(response.status_code, 403)
        self.assertIn("One or more fields missing", response.content.decode())

    def test_03_create_student_with_invalid_degree(self):
        """Test create a student"""

        with open("/home/shivansh/Desktop/all_codes/smart_classroom/smart_classroom_backend/media/teachers/Untitled.jpeg", "rb") as img_file:
            uploaded_image = SimpleUploadedFile(
                "image.jpg", img_file.read() , content_type='image/jpg'
            )

        response = self.client.post("/api/admin/student/create/", {
                "degree_id": 99,
                "first_name": "New",
                "last_name": "Student",
                "phone": "phone",
                "email": "studentemail@school,com",
                "image": uploaded_image,
                "password": "securepassword",
                "semester": 1,
                "roll_number": 230359,
                "category": "General",
                "father_name": "Father Name",
                "mother_name": "Mother Name",
                "father_occupation": "Self Employed",
                "mother_occupation": "House Wife",
                "parent_phone": "newphone",
                "parent_email": "parentemail@school.com",
        }, format='multipart')

        self.assertEqual(response.status_code, 404)
        self.assertIn("Degree not found", response.content.decode())
    
    def test_04_create_student_with_invalid_request_method(self):
        """Test create a student"""

        with open("/home/shivansh/Desktop/all_codes/smart_classroom/smart_classroom_backend/media/teachers/Untitled.jpeg", "rb") as img_file:
            uploaded_image = SimpleUploadedFile(
                "image.jpg", img_file.read() , content_type='image/jpg'
            )

        response = self.client.get("/api/admin/student/create/", {
                "degree_id": self.degree.id,
                "first_name": "New",
                "last_name": "Student",
                "phone": "phone",
                "email": "studentemail@school,com",
                "image": uploaded_image,
                "password": "securepassword",
                "semester": 1,
                "roll_number": 230359,
                "category": "General",
                "father_name": "Father Name",
                "mother_name": "Mother Name",
                "father_occupation": "Self Employed",
                "mother_occupation": "House Wife",
                "parent_phone": "newphone",
                "parent_email": "parentemail@school.com",
        }, format='multipart')

        self.assertEqual(response.status_code, 405)
        self.assertIn("Invalid request method", response.content.decode())
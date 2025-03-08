import json
import hashlib
from PIL import Image
from io import BytesIO
from smart_classroom.models import * 
from .TestData import APITestData
from django.core.files.uploadedfile import SimpleUploadedFile

class StudentAPITests(APITestData):

    def test_01_create_student(self):
        """Test create a student"""

        image = Image.new("RGB", (100, 100), color=(255, 0, 0))  # Red image
        img_io = BytesIO()
        image.save(img_io, format="JPEG")
        img_io.seek(0)

        uploaded_image = SimpleUploadedFile(
            "image.jpg", img_io.getvalue(), content_type="image/jpeg"
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

        image = Image.new("RGB", (100, 100), color=(255, 0, 0))  # Red image
        img_io = BytesIO()
        image.save(img_io, format="JPEG")
        img_io.seek(0)

        uploaded_image = SimpleUploadedFile(
            "image.jpg", img_io.getvalue(), content_type="image/jpeg"
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

        response = self.client.get("/api/admin/student/create/", {
                "degree_id": self.degree.id,
                "first_name": "New",
                "last_name": "Student",
                "phone": "phone",
                "email": "studentemail@school,com",
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

    def test_05_create_student_with_invalid_admin(self):
        """Test create a student"""

        response = self.client.post('/api/user/login/', 
        data = {
            'email': 'testuser3@gmail.com',
            'password': 'password'
        }, content_type='application/json')

        self.token = f"Bearer {response.headers.get('ACCESS-TOKEN')}"
        if self.token:
            self.client.defaults['HTTP_AUTHORIZATION'] = self.token
            self.client.defaults['HTTP_USER_ID'] = str(self.user3.id)

        image = Image.new("RGB", (100, 100), color=(255, 0, 0))  # Red image
        img_io = BytesIO()
        image.save(img_io, format="JPEG")
        img_io.seek(0)

        uploaded_image = SimpleUploadedFile(
            "image.jpg", img_io.getvalue(), content_type="image/jpeg"
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

        self.assertEqual(response.status_code, 401)
        self.assertIn("unauthorized access", response.content.decode())

    def test_06_create_student_using_existing_student_details(self):
        """Test create a student using existing student details"""

        image = Image.new("RGB", (100, 100), color=(255, 0, 0))  # Red image
        img_io = BytesIO()
        image.save(img_io, format="JPEG")
        img_io.seek(0)

        uploaded_image = SimpleUploadedFile(
            "image.jpg", img_io.getvalue(), content_type="image/jpeg"
        )

        response = self.client.post("/api/admin/student/create/", {
                "degree_id": self.degree.id,
                "first_name": "New",
                "last_name": "Student",
                "phone": "phone",
                "email": "testuser4@gmail.com",
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

        self.assertEqual(response.status_code, 401)
        self.assertIn("Student already exists", response.content.decode())
        
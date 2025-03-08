import json
import hashlib
from PIL import Image
from io import BytesIO
from smart_classroom.models import * 
from .TestData import APITestData
from django.core.files.uploadedfile import SimpleUploadedFile


class TeacherAPITests(APITestData):

    def test_01_create_teacher(self):
        """Test create a teacher"""

        image = Image.new("RGB", (100, 100), color=(255, 0, 0))  # Red image
        img_io = BytesIO()
        image.save(img_io, format="JPEG")
        img_io.seek(0)

        uploaded_image = SimpleUploadedFile(
            "image.jpg", img_io.getvalue(), content_type="image/jpeg"
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
        self.assertIn("Teacher created successfully", response.content.decode())
    
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

        image = Image.new("RGB", (100, 100), color=(255, 0, 0))  # Red image
        img_io = BytesIO()
        image.save(img_io, format="JPEG")
        img_io.seek(0)

        uploaded_image = SimpleUploadedFile(
            "image.jpg", img_io.getvalue(), content_type="image/jpeg"
        )

        response = self.client.post("/api/admin/teacher/create/", {
            "department_id": 99,
            "first_name": "Some Name",
            "last_name": "for a teacher",
            "image": uploaded_image,
            "phone": "here phone",
            "email": "teacher@school.com",
            "salary": 120000,
            "password": "securepassword",
        }, format='multipart')

        self.assertEqual(response.status_code, 404)
        self.assertIn("Department not found", response.content.decode())
    
    def test_04_create_teacher_with_invalid_request_method(self):
        """Test create a teacher with invalid request method"""

        response = self.client.get("/api/admin/teacher/create/", {
            "department_id": 99,
            "first_name": "Some Name",
            "last_name": "for a teacher",
            "phone": "here phone",
            "email": "teacher@school.com",
            "salary": 120000,
            "password": "securepassword",
        }, format='multipart')

        self.assertEqual(response.status_code, 405)
        self.assertIn("Invalid request method", response.content.decode())

    def test_05_create_teacher_with_invalid_admin(self):
        """Test create a teacher with invalid admin"""

        response = self.client.post('/api/user/login/', 
        data = {
            'email': 'testuser3@gmail.com',
            'password': 'password'
        }, content_type='application/json')

        self.token = f"Bearer {response.headers.get('ACCESS-TOKEN')}"
        if self.token:
            self.client.defaults['HTTP_AUTHORIZATION'] = self.token
            self.client.defaults['HTTP_USER_ID'] = str(self.user3.id)

        response = self.client.post("/api/admin/teacher/create/", {
            "department_id": self.department.id,
            "first_name": "Some Name",
            "last_name": "for a teacher",
            "phone": "here phone",
            "email": "teacher@school.com",
            "salary": 120000,
            "password": "securepassword",
        }, format='multipart')

        self.assertEqual(response.status_code, 401)
        self.assertIn("unauthorized access", response.content.decode())

    def test_06_create_teacher_using_existing_teacher_details(self):
        """Test create a teacher using existing teacher details"""

        image = Image.new("RGB", (100, 100), color=(255, 0, 0))  # Red image
        img_io = BytesIO()
        image.save(img_io, format="JPEG")
        img_io.seek(0)

        uploaded_image = SimpleUploadedFile(
            "image.jpg", img_io.getvalue(), content_type="image/jpeg"
        )

        response = self.client.post("/api/admin/teacher/create/", {
            "department_id": self.department.id,
            "first_name": "Some Name",
            "last_name": "for a teacher",
            "phone": "here phone",
            "email": "testuser3@gmail.com",
            "image": uploaded_image,
            "salary": 120000,
            "password": "securepassword",
        }, format='multipart')

        self.assertEqual(response.status_code, 401)
        self.assertIn("Teacher already exists", response.content.decode())

    def test_07_update_teacher_phone(self):
        """Test update phone of a teacher"""

        response = self.client.post("/api/admin/teacher/update/", {
            "user_id": self.user3.id,
            "new_details": {
                "phone": "7302232878"
            }
        }, content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertIn("Teacher updated successfully", response.content.decode())
    
    def test_08_update_teacher_email_salary(self):
        """Test update email and salary of a teacher"""

        response = self.client.post("/api/admin/teacher/update/", {
            "user_id": self.user3.id,
            "new_details": {
                "email": "newEmail.teacher@school.com",
                'salary': 240000
            }
        }, content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertIn("Teacher updated successfully", response.content.decode())
    
    def test_09_update_teacher_invalid_field(self):
        """Test update invalid field of a teacher"""

        response = self.client.post("/api/admin/teacher/update/", {
            "user_id": self.user3.id,
            "new_details": {
                "invalid field": "invalid value"
            }
        }, content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertIn("invalid field is invalid field", response.content.decode())
    
    def test_10_update_teacher_invalid_request_method(self):
        """Test update teacher with invalid request method"""

        response = self.client.get("/api/admin/teacher/update/", {
            "user_id": self.user3.id,
            "new_details": {
                "email": "newEmail.teacher@school.com",
                'salary': 240000
            }
        }, content_type='application/json')

        self.assertEqual(response.status_code, 405)
        self.assertIn("Invalid request method", response.content.decode())
    
    def test_11_update_teacher_invalid_admin(self):
        """Test update teacher with invalid admin"""

        response = self.client.post('/api/user/login/', 
        data = {
            'email': 'testuser3@gmail.com',
            'password': 'password'
        }, content_type='application/json')

        self.token = f"Bearer {response.headers.get('ACCESS-TOKEN')}"
        if self.token:
            self.client.defaults['HTTP_AUTHORIZATION'] = self.token
            self.client.defaults['HTTP_USER_ID'] = str(self.user3.id)

        response = self.client.post("/api/admin/teacher/update/", {
            "user_id": self.user3.id,
            "new_details": {
                "email": "newEmail.teacher@school.com",
                'salary': 240000
            }
        }, content_type='application/json')

        self.assertEqual(response.status_code, 401)
        self.assertIn("unauthorized access", response.content.decode())
    
    def test_12_update_teacher_for_non_existent_user(self):
        """Test update teacher for non existent teacher"""

        response = self.client.post("/api/admin/teacher/update/", {
            "user_id": 99,
            "new_details": {
                "email": "newEmail.teacher@school.com",
                'salary': 240000
            }
        }, content_type='application/json')

        self.assertEqual(response.status_code, 404)
        self.assertIn("Teacher not found", response.content.decode())
    
    def test_13_update_teacher_for_user_is_not_teacher(self):
        """Test update teacher for user is not teacher"""

        response = self.client.post("/api/admin/teacher/update/", {
            "user_id": self.user4.id,
            "new_details": {
                "email": "newEmail.teacher@school.com",
                'salary': 240000
            }
        }, content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertIn("User is not a teacher", response.content.decode())
    
    def test_14_update_teacher_with_missing_details(self):
        """Test update teacher with missing details"""

        response = self.client.post("/api/admin/teacher/update/", {
            "user_id": self.user3.id
        }, content_type='application/json')

        self.assertEqual(response.status_code, 403)
        self.assertIn("one or more fields missing", response.content.decode())
    
    def test_15_update_teacher_for_unhandled_exceptions(self):
        """Test update teacher for unhandled exceptions"""

        response = self.client.post("/api/admin/teacher/update/", {
            """'user_id': self.user3.id"""
        }, content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertIn("Something went wrong", response.content.decode())

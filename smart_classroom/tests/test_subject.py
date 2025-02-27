import json
import hashlib
from smart_classroom.models import * 
from django.urls import reverse
from django.test import TestCase, Client

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
        
        # user for teacher role
        cls.user2 = User.objects.create(
        first_name='first_name', 
        last_name='last_name', 
        phone='phone', 
        email='testuser2@gmail.com', 
        role='teacher', 
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

        # create a course
        cls.course = Course.objects.create(
            degree=cls.degree,
            name="Discipline Specific Core",
            total_credits=4
        )

        # create a teacher
        cls.teacher = Teacher.objects.create(
            user=cls.user2,
            department=cls.department,
            image="None",
            salary=120000
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

    def test_01_create_subject(self):
        """Test create subject"""

        response = self.client.post("/api/admin/subject/create/", {
                "course_id": self.course.id,            
                "teacher_id": self.teacher.id,            
                "name": "C++ Basics",            
                "semester": 1,        
        }, content_type='application/json')

        self.assertEqual(response.status_code, 201)
        self.assertIn("Subject created successfully", response.content.decode())

    def test_02_create_subject_with_incomplete_details(self):
        """Test create subject with incomplete details"""

        response = self.client.post("/api/admin/subject/create/", {
                "course_id": self.course.id,            
                "teacher_id": self.teacher.id,            
                "name": "C++ Basics", 
        }, content_type='application/json')

        self.assertEqual(response.status_code, 403)
        self.assertIn("one or more fields missing", response.content.decode())
    
    def test_03_create_subject_without_teacher(self):
        """Test create subject with incomplete details"""

        response = self.client.post("/api/admin/subject/create/", {
                "course_id": self.course.id,        
                "name": "C++ Basics",
                "semester": 1, 
        }, content_type='application/json')

        self.assertEqual(response.status_code, 201)
        self.assertIn("Subject created successfully", response.content.decode())
    
    def test_04_create_subject_with_invalid_teacher(self):
        """Test create subject with incomplete details"""

        response = self.client.post("/api/admin/subject/create/", {
                "course_id": self.course.id,
                "teacher_id": 99,       
                "name": "C++ Basics", 
                "semester": 1,
        }, content_type='application/json')

        self.assertEqual(response.status_code, 404)
        self.assertIn("Teacher not found", response.content.decode())
    
    def test_05_create_subject_with_invalid_course(self):
        """Test create subject with incomplete details"""

        response = self.client.post("/api/admin/subject/create/", {
                "course_id": 99,
                "teacher_id": self.teacher.id,       
                "name": "C++ Basics", 
                "semester": 1,
        }, content_type='application/json')

        self.assertEqual(response.status_code, 404)
        self.assertIn("Course not found", response.content.decode())

    def test_06_create_subject_with_invalid_request_method(self):
        """Test create subject"""

        response = self.client.get("/api/admin/subject/create/", {
                "course_id": self.course.id,            
                "teacher_id": self.teacher.id,            
                "name": "C++ Basics",            
                "semester": 1,        
        }, content_type='application/json')

        self.assertEqual(response.status_code, 405)
        self.assertIn("Invalid request method", response.content.decode())
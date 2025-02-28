import json
import hashlib
from smart_classroom.models import * 
from django.test import TestCase, Client

class APITestData(TestCase):

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
        role='admin', 
        password=hashlib.sha256('password'.encode()).hexdigest())
                
        # user for student role
        cls.user3 = User.objects.create(
        first_name='first_name', 
        last_name='last_name', 
        phone='phone', 
        email='testuser3@gmail.com', 
        role='teacher', 
        password=hashlib.sha256('password'.encode()).hexdigest())
        
        cls.user4 = User.objects.create(
        first_name='first_name', 
        last_name='last_name', 
        phone='phone', 
        email='testuser4@gmail.com', 
        role='student', 
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
            user=cls.user3,
            department=cls.department,
            image="None",
            salary=120000
        )

        # create a student
        cls.student = Student.objects.create(
            user=cls.user4,
            degree = cls.degree,
            semester = 1,
            roll_number = 230259,
            category = "category",
            image="None",
            father_name = "father_name",
            mother_name = "mother_name",
            father_occupation = "father_occupation",
            mother_occupation = "mother_occupation",
            parent_phone = "parent_phone",
            parent_email = "parent_email",
        )

    def setUp(self):

        self.client = Client()
        response = self.client.post('/api/user/login/', 
        data = {
            'email': 'testuser@gmail.com',
            'password': 'password'
        }, content_type='application/json')

        self.token = f"Bearer {response.headers.get('ACCESS-TOKEN')}"
        if self.token:
            self.client.defaults['HTTP_AUTHORIZATION'] = self.token
            self.client.defaults['HTTP_USER_ID'] = str(self.user.id)

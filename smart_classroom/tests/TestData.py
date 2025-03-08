import os
import json
import shutil
import hashlib
from PIL import Image
from io import BytesIO
from django.conf import settings
from smart_classroom.models import *
from django.test import override_settings, TestCase, Client

TEST_MEDIA_ROOT = os.path.join(settings.BASE_DIR, "test_media")

@override_settings(MEDIA_ROOT=TEST_MEDIA_ROOT)
class APITestData(TestCase):

    @classmethod
    def setUpTestData(cls):

        # create organisation for the user
        cls.organisation = Organisation.objects.create(
            name='First Organisation',
            orgType='Private School'
        )

        # user for admin role
        cls.user = User.objects.create(
        organisation=cls.organisation,
        first_name='first_name', 
        last_name='last_name', 
        phone='phone', 
        email='testuser@gmail.com', 
        role='admin', 
        password=hashlib.sha256('password'.encode()).hexdigest())
        
        cls.user2 = User.objects.create(
        first_name='first_name', 
        last_name='last_name', 
        phone='phone', 
        email='testuser2@gmail.com', 
        role='admin', 
        password=hashlib.sha256('password'.encode()).hexdigest())
                
        # user for teacher role
        cls.user3 = User.objects.create(
        organisation=cls.organisation,
        first_name='first_name', 
        last_name='last_name', 
        phone='phone', 
        email='testuser3@gmail.com', 
        role='teacher', 
        password=hashlib.sha256('password'.encode()).hexdigest())
        
        # user for student role
        cls.user4 = User.objects.create(
        organisation=cls.organisation,
        first_name='first_name', 
        last_name='last_name', 
        phone='phone', 
        email='testuser4@gmail.com', 
        role='student', 
        password=hashlib.sha256('password'.encode()).hexdigest())

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

        # create a subject
        cls.subject = Subject.objects.create(
            name='Subject name',
            semester=1
        )
        cls.subject.course.set([cls.course])
        cls.subject.save()

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
        
    @classmethod
    def setUpClass(cls):
        """Create test media folder before tests run."""
        super().setUpClass()
        os.makedirs(TEST_MEDIA_ROOT, exist_ok=True)

    @classmethod
    def tearDownClass(cls):
        """Delete test media folder after all tests finish."""
        super().tearDownClass()
        shutil.rmtree(TEST_MEDIA_ROOT, ignore_errors=True)

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

class ModelTestData(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        cls.org = Organisation.objects.create(name='Test Org', orgType='Private')
        cls.user1 = User.objects.create(organisation=cls.org, first_name='org', last_name='user', phone='1478523699', email='orguser@example.com', password='password123')
        cls.user2 = User.objects.create(organisation=cls.org, first_name='teacher', last_name='user', phone='4569877412', email='teacheruser@example.com', password='password123')
        cls.user3 = User.objects.create(organisation=cls.org, first_name='student', last_name='user', phone='1236548521', email='studentuser@example.com', password='password123')
        cls.department = Department.objects.create(organisation=cls.org, name='Engineering')
        cls.degree = Degree.objects.create(department=cls.department, title='B.Tech', branch='CSE', semesters=8)
        cls.course = Course.objects.create(degree=cls.degree, name="Discipline Specific Core", total_credits=4)
        cls.subject = Subject.objects.create(name="C++ Basics", semester=1)
        cls.subject.course.set([cls.course])
        cls.teacher = Teacher.objects.create(user=cls.user2, department=cls.department, salary=50000)
        cls.student = Student.objects.create(user=cls.user3, degree=cls.degree, semester=1, roll_number=1001, parent_phone='1234567890', parent_email='parent@example.com')
        cls.result = Result.objects.create(student=cls.student, semester=1, subject=cls.subject, grade="A", gained_credit=4)
        cls.address = UserAddress.objects.create(user=cls.user1, addressname='Home', city='New York', zipcode=10001)

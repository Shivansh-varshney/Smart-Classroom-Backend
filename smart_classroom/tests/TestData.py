import os
import json
import shutil
import hashlib
from django.conf import settings
from smart_classroom.models import *
from django.test import override_settings, TestCase, Client

TEST_MEDIA_ROOT = os.path.join(settings.BASE_DIR, "test_media")

class ModelTestData(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.organisation = Organisation.objects.create(name='First Organisation',orgType='Private School')
        cls.user = User.objects.create(organisation=cls.organisation,first_name='first_name', last_name='last_name', phone='phone', email='testuser@gmail.com', role='admin', password=hashlib.sha256('password'.encode()).hexdigest())        
        cls.user2 = User.objects.create(first_name='first_name', last_name='last_name', phone='phone', email='testuser2@gmail.com', role='admin', password=hashlib.sha256('password'.encode()).hexdigest())                
        cls.user3 = User.objects.create(organisation=cls.organisation,first_name='first_name', last_name='last_name', phone='phone', email='testuser3@gmail.com', role='teacher', password=hashlib.sha256('password'.encode()).hexdigest())        
        cls.user4 = User.objects.create(organisation=cls.organisation,first_name='first_name', last_name='last_name', phone='phone', email='testuser4@gmail.com', role='student', password=hashlib.sha256('password'.encode()).hexdigest())
        cls.department = Department.objects.create(organisation=cls.organisation,name="Computer Science")
        cls.degree = Degree.objects.create(department=cls.department,title="Bachelor Of Science",branch="Computer Science",semesters=8)
        cls.course = Course.objects.create(degree=cls.degree,name="Discipline Specific Core",total_credits=4)
        cls.subject = Subject.objects.create(name='Subject name',semester=1)
        cls.subject.course.set([cls.course])
        cls.teacher = Teacher.objects.create(user=cls.user3,department=cls.department,image="None",salary=120000)
        cls.student = Student.objects.create(user=cls.user4,degree = cls.degree,semester = 1,roll_number = 230259,category = "category",image="None",father_name = "father_name",mother_name = "mother_name",father_occupation = "father_occupation",mother_occupation = "mother_occupation",parent_phone = "parent_phone",parent_email = "parent_email",)
        cls.result = Result.objects.create(student=cls.student, semester=1, subject=cls.subject, grade="A", gained_credit=4)
        cls.address = UserAddress.objects.create(user=cls.user,house_number="123A",street="Main Street",city="New York",district="Manhattan",state="NY",country="USA",zipcode=10001)

@override_settings(MEDIA_ROOT=TEST_MEDIA_ROOT)
class APITestData(ModelTestData):
        
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

        self.otp = EmailOTP.objects.create(email='testuser@gmail.com', otp=hashlib.sha256('000111'.encode()).hexdigest())

        self.client = Client()
        response = self.client.post('/api/user/verify-otp/', 
        data = {
            'email': 'testuser@gmail.com',
            'otp': '000111'
        }, content_type='application/json')

        self.token = f"Bearer {response.headers.get('ACCESS-TOKEN')}"
        self.refresh_token = f"{response.headers.get('REFRESH-TOKEN')}"
        if self.token:
            self.client.defaults['HTTP_AUTHORIZATION'] = self.token
            self.client.defaults['HTTP_USER_ID'] = str(self.user.id)

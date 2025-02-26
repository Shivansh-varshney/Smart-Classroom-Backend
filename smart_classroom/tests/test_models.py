from smart_classroom.models import *
from django.test import TestCase, Client
from django.core.exceptions import ValidationError

class UserModelTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='password123',
            first_name='Test',
            last_name='User',
            phone='1234567890',
            role='admin'
        )
    
    def test_01_user_creation(self):
        """Test if a user is created properly."""
        self.assertEqual(self.user.email, 'testuser@example.com')
    
    def test_02_user_str(self):
        """Test user string representation."""
        self.assertEqual(str(self.user), 'Test User')

    def test_03_duplicate_username(self):
        """Test that duplicate usernames are not allowed."""
        with self.assertRaises(Exception):
            User.objects.create_user(username='testuser', email='new@example.com', password='password123')

class OrganisationModelTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='orguser', email='orguser@example.com', password='password123')
        self.org = Organisation.objects.create(user=self.user, name='Test Org', orgType='Private')
    
    def test_01_organisation_creation(self):
        """Test if an organisation is created properly."""
        self.assertEqual(self.org.name, 'Test Org')
    
    def test_02_organisation_str(self):
        """Test organisation string representation."""
        self.assertEqual(str(self.org), 'Test Org')

class DepartmentModelTestCase(TestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(username='deptuser', email='deptuser@example.com', password='password123')
        self.org = Organisation.objects.create(user=self.user, name='Test Org', orgType='Public')
        self.department = Department.objects.create(organisation=self.org, name='Computer Science')
    
    def test_01_department_creation(self):
        """Test if a department is created properly."""
        self.assertEqual(self.department.name, 'Computer Science')
    
    def test_02_department_str(self):
        """Test department string representation."""
        self.assertEqual(str(self.department), 'Computer Science Department, Test Org')

class DegreeModelTestCase(TestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(username='degreeuser', email='degreeuser@example.com', password='password123')
        self.org = Organisation.objects.create(user=self.user, name='Test Org', orgType='Private')
        self.department = Department.objects.create(organisation=self.org, name='Engineering')
        self.degree = Degree.objects.create(department=self.department, title='B.Tech', branch='CSE', semesters=8)
    
    def test_01_degree_creation(self):
        """Test if a degree is created properly."""
        self.assertEqual(self.degree.title, 'B.Tech')
    
    def test_02_degree_str(self):
        """Test degree string representation."""
        self.assertEqual(str(self.degree), 'B.Tech CSE, Test Org')
    
    def test_03_invalid_semesters(self):
        """Test that an invalid semester count raises an error."""
        with self.assertRaises(ValidationError):
            degree = Degree(department=self.department, title='M.Tech', branch='ECE', semesters=-1)
            degree.full_clean()

class StudentModelTestCase(TestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(username='studentuser', email='studentuser@example.com', password='password123')
        self.org = Organisation.objects.create(user=self.user, name='Test Org', orgType='Public')
        self.department = Department.objects.create(organisation=self.org, name='Science')
        self.degree = Degree.objects.create(department=self.department, title='B.Sc', branch='Physics', semesters=6)
        self.student = Student.objects.create(user=self.user, degree=self.degree, semester=1, roll_number=1001, parent_phone='1234567890', parent_email='parent@example.com')
    
    def test_01_student_creation(self):
        """Test if a student is created properly."""
        self.assertEqual(self.student.roll_number, 1001)
    
    def test_02_student_str(self):
        """Test student string representation."""
        self.assertEqual(str(self.student), 'Student: studentuser@example.com')

class TeacherModelTestCase(TestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(username='teacheruser', email='teacheruser@example.com', password='password123')
        self.department = Department.objects.create(name='Mathematics', organisation=Organisation.objects.create(user=self.user, name='Test Org', orgType='Private'))
        self.teacher = Teacher.objects.create(user=self.user, department=self.department, salary=50000)
    
    def test_01_teacher_creation(self):
        """Test if a teacher is created properly."""
        self.assertEqual(self.teacher.salary, 50000)
    
    def test_02_teacher_str(self):
        """Test teacher string representation."""
        self.assertEqual(str(self.teacher), 'Teacher: teacheruser@example.com')
    
    def test_03_negative_salary(self):
        """Test that negative salary is not allowed."""
        with self.assertRaises(ValidationError):
            teacher = Teacher(user=self.user, department=self.department, salary=-1000)
            teacher.full_clean()

class UserAddressModelTestCase(TestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(username='addressuser', email='addressuser@example.com', password='password123')
        self.address = UserAddress.objects.create(user=self.user, addressname='Home', city='New York', zipcode=10001)
    
    def test_01_user_address_creation(self):
        """Test if a user address is created properly."""
        self.assertEqual(self.address.city, 'New York')
    
    def test_02_user_address_str(self):
        """Test user address string representation."""
        self.assertEqual(self.address.addressname, 'Home')

    def test_03_invalid_zipcode(self):
        """Test that an invalid zipcode raises an error."""
        with self.assertRaises(ValidationError):
            address = UserAddress(user=self.user, addressname='Office', city='Boston', zipcode='ABCDE')
            address.full_clean()

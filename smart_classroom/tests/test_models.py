from smart_classroom.models import *
from django.test import TestCase, Client
from django.core.exceptions import ValidationError

class BaseDataSet(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        cls.user1 = User.objects.create(first_name='org', last_name='user', phone='1478523699', email='orguser@example.com', password='password123')
        cls.user2 = User.objects.create(first_name='teacher', last_name='user', phone='4569877412', email='teacheruser@example.com', password='password123')
        cls.user3 = User.objects.create(first_name='student', last_name='user', phone='1236548521', email='studentuser@example.com', password='password123')
        cls.org = Organisation.objects.create(user=cls.user1, name='Test Org', orgType='Private')
        cls.department = Department.objects.create(organisation=cls.org, name='Engineering')
        cls.degree = Degree.objects.create(department=cls.department, title='B.Tech', branch='CSE', semesters=8)
        cls.course = Course.objects.create(degree=cls.degree, name="Discipline Specific Core", total_credits=4)
        cls.subject = Subject.objects.create(name="C++ Basics", semester=1)
        cls.subject.course.set([cls.course])
        cls.teacher = Teacher.objects.create(user=cls.user2, department=cls.department, salary=50000)
        cls.student = Student.objects.create(user=cls.user3, degree=cls.degree, semester=1, roll_number=1001, parent_phone='1234567890', parent_email='parent@example.com')
        cls.result = Result.objects.create(student=cls.student, semester=1, subject=cls.subject, grade="A", gained_credit=4)
        cls.address = UserAddress.objects.create(user=cls.user1, addressname='Home', city='New York', zipcode=10001)

class UserModelTestCase(BaseDataSet):
    
    def test_01_user_creation(self):
        """Test if a user is created properly."""
        self.assertEqual(self.user1.email, 'orguser@example.com')
    
    def test_02_user_str(self):
        """Test user string representation."""
        self.assertEqual(str(self.user1), 'org user')

class OrganisationModelTestCase(BaseDataSet):
    
    def test_01_organisation_creation(self):
        """Test if an organisation is created properly."""
        self.assertEqual(self.org.name, 'Test Org')
    
    def test_02_organisation_str(self):
        """Test organisation string representation."""
        self.assertEqual(str(self.org), 'Test Org')

class DepartmentModelTestCase(BaseDataSet):
    
    def test_01_department_creation(self):
        """Test if a department is created properly."""
        self.assertEqual(self.department.name, 'Engineering')
    
    def test_02_department_str(self):
        """Test department string representation."""
        self.assertEqual(str(self.department), 'Engineering Department, Test Org')

class DegreeModelTestCase(BaseDataSet):
    
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

class CourseModelTestCase(BaseDataSet):
   
    def test_01_course_creation(self):
        """Test course is created properly"""
        self.assertEqual(self.course.name, "Discipline Specific Core")

    def test_02_course_str(self):
        """Test course string representation"""
        self.assertEqual(str(self.course), "Discipline Specific Core, Engineering Department, Test Org")

class SubjectModelTestCase(BaseDataSet):

    def test_01_subject_creation(self):
        self.assertEqual(self.subject.name, "C++ Basics")

    def test_02_subject_str(self):
        self.assertEqual(str(self.subject), "C++ Basics")

class ResultModelTestCase(BaseDataSet):

    def test_01_subject_creation(self):
        self.assertEqual(self.result.subject.name, "C++ Basics")

    def test_02_subject_str(self):
        self.assertEqual(str(self.result), "Roll Number: 1001, Semester: 1, Subject: C++ Basics")

class StudentModelTestCase(BaseDataSet):
    
    def test_01_student_creation(self):
        """Test if a student is created properly."""
        self.assertEqual(self.student.roll_number, 1001)
    
    def test_02_student_str(self):
        """Test student string representation."""
        self.assertEqual(str(self.student), 'Student: studentuser@example.com')

class TeacherModelTestCase(BaseDataSet):
   
    def test_01_teacher_creation(self):
        """Test if a teacher is created properly."""
        self.assertEqual(self.teacher.salary, 50000)
    
    def test_02_teacher_str(self):
        """Test teacher string representation."""
        self.assertEqual(str(self.teacher), 'Teacher: teacheruser@example.com')
    
    def test_03_negative_salary(self):
        """Test that negative salary is not allowed."""
        with self.assertRaises(ValidationError):
            teacher = Teacher(user=self.user2, department=self.department, salary=-1000)
            teacher.full_clean()

class UserAddressModelTestCase(BaseDataSet):
    
    def test_01_user_address_creation(self):
        """Test if a user address is created properly."""
        self.assertEqual(self.address.city, 'New York')
    
    def test_02_user_address_str(self):
        """Test user address string representation."""
        self.assertEqual(self.address.addressname, 'Home')

    def test_03_invalid_zipcode(self):
        """Test that an invalid zipcode raises an error."""
        with self.assertRaises(ValidationError):
            address = UserAddress(user=self.user1, addressname='Office', city='Boston', zipcode='ABCDE')
            address.full_clean()

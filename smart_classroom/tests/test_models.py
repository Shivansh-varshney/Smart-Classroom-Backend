from smart_classroom.models import *
from django.test import TestCase, Client
from django.core.exceptions import ValidationError
from .TestData import ModelTestData

class UserModelTestCase(ModelTestData):
    def test_user_creation(self):
        self.assertEqual(self.user.email, 'testuser@gmail.com')
    
    def test_user_str(self):
        self.assertEqual(str(self.user), 'first_name last_name')

class OrganisationModelTestCase(ModelTestData):
    def test_organisation_creation(self):
        self.assertEqual(self.organisation.name, 'First Organisation')
    
    def test_organisation_str(self):
        self.assertEqual(str(self.organisation), 'First Organisation')

class DepartmentModelTestCase(ModelTestData):
    def test_department_creation(self):
        self.assertEqual(self.department.name, 'Computer Science')
    
    def test_department_str(self):
        self.assertEqual(str(self.department), 'Computer Science Department, First Organisation')

class DegreeModelTestCase(ModelTestData):
    def test_degree_creation(self):
        self.assertEqual(self.degree.title, 'Bachelor Of Science')
    
    def test_degree_str(self):
        self.assertEqual(str(self.degree), 'Bachelor Of Science Computer Science, First Organisation')
    
    def test_invalid_semesters(self):
        with self.assertRaises(ValidationError):
            degree = Degree(department=self.department, title='M.Tech', branch='ECE', semesters=-1)
            degree.full_clean()

class CourseModelTestCase(ModelTestData):
    def test_course_creation(self):
        self.assertEqual(self.course.name, "Discipline Specific Core")
    
    def test_course_str(self):
        self.assertEqual(str(self.course), "Discipline Specific Core, Computer Science Department, First Organisation")

class SubjectModelTestCase(ModelTestData):
    def test_subject_creation(self):
        self.assertEqual(self.subject.name, "Subject name")
    
    def test_subject_str(self):
        self.assertEqual(str(self.subject), "Subject name")

class ResultModelTestCase(ModelTestData):
    def test_result_creation(self):
        self.assertEqual(self.result.subject.name, "Subject name")
    
    def test_result_str(self):
        self.assertEqual(str(self.result), "Roll Number: 230259, Semester: 1, Subject: Subject name")

class StudentModelTestCase(ModelTestData):
    def test_student_creation(self):
        self.assertEqual(self.student.roll_number, 230259)
    
    def test_student_str(self):
        self.assertEqual(str(self.student), 'Student: testuser4@gmail.com')

class TeacherModelTestCase(ModelTestData):
    def test_teacher_creation(self):
        self.assertEqual(self.teacher.salary, 120000)
    
    def test_teacher_str(self):
        self.assertEqual(str(self.teacher), 'Teacher: testuser3@gmail.com')
    
    def test_negative_salary(self):
        with self.assertRaises(ValidationError):
            teacher = Teacher(user=self.user2, department=self.department, salary=-1000)
            teacher.full_clean()

class UserAddressModelTestCase(ModelTestData):
    def test_user_address_creation(self):
        self.assertEqual(self.address.city, 'New York')
    
    def test_user_address_str(self):
        self.assertEqual(self.address.city, 'New York')
    
    def test_invalid_zipcode(self):
        with self.assertRaises(ValidationError):
            address = UserAddress(user=self.user, city='Boston', zipcode='ABCDE')
            address.full_clean()

from django.db import models
from django.contrib.auth.models import AbstractUser

organisationType = {
    "Private School": "Private School",
    "Private College": "Private College",
    "Government School": "Government School",
    "Government College": "Government College",
    "Semi-government School": "Semi-government School",
    "Semi-government College": "Semi-government College",
    "Central Government School": "Central Government School",
    "Central Government College": "Central Government College",
    "International School": "International School",
    "Autonomous College": "Autonomous College",
    "Deemed University": "Deemed University",
    "State University": "State University",
    "Central University": "Central University",
    "Private University": "Private University",
    "Open University": "Open University",
    "Distance Learning Institute": "Distance Learning Institute",
    "Vocational Training Institute": "Vocational Training Institute",
    "Polytechnic College": "Polytechnic College",
    "Engineering College": "Engineering College",
    "Medical College": "Medical College",
    "Law College": "Law College",
    "Management Institute": "Management Institute",
    "Research Institute": "Research Institute"
}

boards = {
    "CBSE: Central Board of Secondary Education": "CBSE: Central Board of Secondary Education",
    "ICSE: Indian Certificate of Secondary Education": "ICSE: Indian Certificate of Secondary Education",
    "NIOS: National Institute of Open Schooling": "NIOS: National Institute of Open Schooling",
    "CISCE: Council for the Indian School Certificate Examinations": "CISCE: Council for the Indian School Certificate Examinations",
    "IB: International Baccalaureate": "IB: International Baccalaureate",
    "IGCSE: International General Certificate of Secondary Education": "IGCSE: International General Certificate of Secondary Education",
    "Cambridge: Cambridge Assessment International Education": "Cambridge: Cambridge Assessment International Education",
    "Madarsa: Madarsa Education Board": "Madarsa: Madarsa Education Board",
    "WBBSE: West Bengal Board of Secondary Education": "WBBSE: West Bengal Board of Secondary Education",
    "MSBSHSE: Maharashtra State Board of Secondary and Higher Secondary Education": "MSBSHSE: Maharashtra State Board of Secondary and Higher Secondary Education",
    "UPMSP: Uttar Pradesh Madhyamik Shiksha Parishad": "UPMSP: Uttar Pradesh Madhyamik Shiksha Parishad",
    "RBSE: Rajasthan Board of Secondary Education": "RBSE: Rajasthan Board of Secondary Education",
    "PSEB: Punjab School Education Board": "PSEB: Punjab School Education Board",
    "BSEB: Bihar School Examination Board": "BSEB: Bihar School Examination Board",
    "GSEB: Gujarat Secondary and Higher Secondary Education Board": "GSEB: Gujarat Secondary and Higher Secondary Education Board",
    "KSEEB: Karnataka Secondary Education Examination Board": "KSEEB: Karnataka Secondary Education Examination Board",
    "TNBSE: Tamil Nadu Board of Secondary Education": "TNBSE: Tamil Nadu Board of Secondary Education",
    "APBSE: Andhra Pradesh Board of Secondary Education": "APBSE: Andhra Pradesh Board of Secondary Education",
    "HBSE: Haryana Board of School Education": "HBSE: Haryana Board of School Education",
    "MPBSE: Madhya Pradesh Board of Secondary Education": "MPBSE: Madhya Pradesh Board of Secondary Education",
    "CGBSE: Chhattisgarh Board of Secondary Education": "CGBSE: Chhattisgarh Board of Secondary Education",
    "JKBOSE: Jammu and Kashmir State Board of School Education": "JKBOSE: Jammu and Kashmir State Board of School Education",
    "MBOSE: Meghalaya Board of School Education": "MBOSE: Meghalaya Board of School Education",
    "NBSE: Nagaland Board of School Education": "NBSE: Nagaland Board of School Education",
    "BSE Odisha: Board of Secondary Education, Odisha": "BSE Odisha: Board of Secondary Education, Odisha"
}

roles = {
    'admin': 'admin',
    'student': 'student',
    'teacher': 'teacher'
}

class User(AbstractUser):

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    role = models.CharField(choices=roles, max_length=15, default='admin')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return f"{self.first_name} {self.last_name}" if self.first_name else self.email

class Organisation(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=256)
    orgType = models.CharField(choices=organisationType, max_length=256)
    board = models.CharField(choices=boards, max_length=256, null=True, blank=True)

    def __str__(self):
        return self.name

class Department(models.Model):

    organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE)
    name = models.CharField(max_length=256)
    subjects = models.ManyToManyField('Subject', blank=True)

    def __str__(self):
        return f"{self.name} Department, {self.organisation}"

    class Meta:
        verbose_name_plural = "Departments"

class Degree(models.Model):

    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    title = models.CharField(max_length=256)
    branch = models.CharField(max_length=256)
    semesters = models.IntegerField()

    def __str__(self):
        return f"{self.title} {self.branch}, {self.department.organisation}"

class Course(models.Model):

    degree = models.ForeignKey(Degree, on_delete=models.CASCADE)
    name = models.CharField(max_length=256)
    total_credits = models.IntegerField()

    def __str__(self):
        return f"{self.name}, {self.degree.department.name} Department, {self.degree.department.organisation}"

class Subject(models.Model):

    course = models.ManyToManyField('Course', blank=True)
    teacher = models.ManyToManyField('Teacher', blank=True)
    name = models.CharField(max_length=20)
    semester = models.IntegerField()

    def __str__(self):
        return f"{self.name}"

class Student(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    degree = models.OneToOneField(Degree, on_delete=models.CASCADE)
    subjects = models.ManyToManyField('Subject', blank=True)
    image = models.ImageField(upload_to='media/students/')
    semester = models.IntegerField()
    roll_number = models.IntegerField()
    parent_phone = models.CharField(max_length=12)
    parent_email = models.EmailField()

    def __str__(self):
        return f"Student: {self.user.email}"

class Teacher(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='media/teachers/')
    salary = models.IntegerField()

    def __str__(self):
        return f"Teacher: {self.user.email}"

class Result(models.Model):

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    semester = models.IntegerField()
    grade = models.CharField(max_length=3)
    gained_credit = models.IntegerField()

    def __str__(self):
        return f"Roll Number: {self.student.roll_number}, Semester: {self.semester}, Subject: {self.subject}"
   
class UserAddress(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE)
    addressname = models.CharField(
        max_length=50, null=True, blank=True)
    housenumber = models.CharField(
        max_length=50, unique=True, null=True, blank=True)
    landmark = models.CharField(
        max_length=50, null=True, blank=True)
    street = models.CharField(
        max_length=250, null=True, blank=True)
    city = models.CharField(
        max_length=250, null=True, blank=True)
    district = models.CharField(
        max_length=250, null=True, blank=True)
    state = models.CharField(
        max_length=250, null=True, blank=True)
    country = models.CharField(
        max_length=250, null=True, blank=True)
    zipcode = models.IntegerField(null=True, blank=True)
    status = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "User Adresses"

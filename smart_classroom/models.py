from django.db import models
from datetime import timedelta
from django.utils import timezone
from shortuuid.django_fields import ShortUUIDField
from django.core.validators import MinValueValidator
from django.contrib.auth.models import AbstractUser

requestStatus = {
    'Pending': 'Pending',
    'In process': 'In process',
    'Resolved': 'Resolved'
}

class Organisation(models.Model):

    name = models.CharField(max_length=256)
    orgType = models.CharField(max_length=256)
    board = models.CharField(max_length=256, null=True, blank=True)

    def __str__(self):
        return self.name

class User(AbstractUser):

    username = models.CharField(max_length=256, null=True, blank=True)
    organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE, null=True, blank=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=15, default='admin')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return f"{self.first_name} {self.last_name}" if self.first_name else self.email

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
    semesters = models.IntegerField(validators=[MinValueValidator(1)])

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
    degree = models.ForeignKey(Degree, on_delete=models.CASCADE)
    subjects = models.ManyToManyField('Subject', blank=True)
    image = models.ImageField(upload_to='media/students/')
    semester = models.IntegerField()
    roll_number = models.IntegerField()
    category = models.CharField(max_length=256)
    father_name = models.CharField(max_length=256)
    mother_name = models.CharField(max_length=256)
    father_occupation = models.CharField(max_length=256)
    mother_occupation = models.CharField(max_length=256)
    parent_phone = models.CharField(max_length=15)
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
        return f"Roll Number: {self.student.roll_number}, Semester: {self.semester}, Subject: {self.subject.name}"
   
class UserAddress(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE)
    house_number = models.CharField(
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

    class Meta:
        verbose_name_plural = "User Adresses"

class ContactRequest(models.Model):

    requestID = ShortUUIDField(unique=True, length=14, max_length=15, alphabet="ABCDEFGHIGKLMNOPQRSTUVWXYZ1234567890")
    status = models.CharField(choices=requestStatus, default='Pending', max_length=12)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.CharField(max_length=256, null=False, blank=False)
    phone = models.CharField(max_length=15, null=False, blank=False)
    topic = models.CharField(max_length=50, null=False, blank=False)
    description = models.TextField(null=False, blank=False)

    def __str__(self):
        return f"Request ID: {self.requestID}"

class EmailOTP(models.Model):

    email = models.EmailField()
    otp = models.CharField(max_length=256)
    createdAt = models.DateTimeField(auto_now_add=True)

    def is_expired(self):
        return self.createdAt < timezone.now() - timedelta(minutes=10)
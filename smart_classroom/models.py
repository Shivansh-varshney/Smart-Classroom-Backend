from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    division = models.CharField(max_length=3)
    section = models.CharField(max_length=3)
    phone = models.CharField(max_length=12)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=256, default='admin')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return f"{self.first_name} {self.last_name}" if self.first_name else self.email

class Student(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    roll_number = models.IntegerField()
    parent_phone = models.CharField(max_length=12)
    parent_email = models.EmailField()
    subjects = models.ManyToManyField('Subject')

    def __str__(self):
        return f"Student: {user.email}"

class Teacher(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    salary = models.IntegerField()
    subjects = models.ManyToManyField('Subject')

    def __str__(self):
        return f"Teacher: {user.email}"

class Subject(models.Model):

    name = models.CharField(max_length=20)

    def __str__(self):
        return f"Subject: {self.name}"

class Result(models.Model):

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subjects = models.ForeignKey(Subject, on_delete=models.CASCADE)
    grade = models.CharField(max_length=5)
    name_Of_Test = models.CharField(max_length=30)

    def __str__(self):
        return f"Student: {student.user.email}, Test: {self.name_Of_Test}"

class userAddress(models.Model):
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

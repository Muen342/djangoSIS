# Create your models here.
from django.db import models
from django.utils import timezone
import datetime

class Locker(models.Model):
    id = models.IntegerField(primary_key=True)
    location = models.CharField(max_length=50)
    active = models.BooleanField(default=False)
    combination = models.CharField(max_length=20)

class Student(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    grade = models.IntegerField(default=0)
    locker = models.ForeignKey(Locker, on_delete=models.CASCADE, default=0)

class Teacher(models.Model):
    id = models.CharField(primary_key=True, max_length=20)
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    department = models.CharField(max_length=50)

class Courses(models.Model):
    code = models.CharField(max_length=30, default='')
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    title = models.CharField(max_length=30)
    credit = models.DecimalField(default=0, decimal_places=2, max_digits=3)
    description = models.TextField(max_length=500)
    students = models.TextField(max_length=500, default='')

class Assignment(models.Model):
    course = models.ForeignKey(Courses, on_delete=models.CASCADE)
    outof = models.IntegerField(default=0)
    weight = models.DecimalField(default=0, decimal_places=2, max_digits=5)
    title = models.CharField(max_length=50)
    category = models.CharField(max_length=20)

class Marks(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    mark = models.IntegerField(default=0)

class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Courses, on_delete=models.CASCADE)
    date = models.DateField(default = datetime.datetime.today)

    ATTENDANCE_STATUS = (
        ('A', 'Absent'),
        ('P', 'Present'),
        ('E', 'Excused'),
    )

    attendance = models.CharField(
        max_length=1,
        choices=ATTENDANCE_STATUS,
        blank=True,
        default='P',
        help_text='Attendance',
    )
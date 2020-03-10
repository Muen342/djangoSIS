from django.contrib import admin
from .models import Student, Locker, Teacher, Courses, Assignment, Marks
# Register your models here.
admin.site.register(Student)
admin.site.register(Locker)
admin.site.register(Teacher)
admin.site.register(Courses)
admin.site.register(Assignment)
admin.site.register(Marks)
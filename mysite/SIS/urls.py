from django.urls import path

from . import views

app_name = 'SIS'
urlpatterns = [
    path('', views.index, name='index'),
    path('students/', views.studentIndex, name='studentIndex'),
    path('students/list/<int:student_id>/', views.detail, name='detail'),
    path('students/list/<int:student_id>/edit', views.editStudent, name='editStudent'),
    path('students/list/<int:student_id>/confirmStudent/', views.confirmStudent, name='confirmStudent'),
    path('students/add/', views.addStudent, name='addStudent'),
    path('students/list/', views.listStudents, name='listStudents'),
    path('students/add/confirm', views.addStudentConfirm, name='addStudentConfirm'),
    path('courses/', views.coursesIndex, name='coursesIndex'),
    path('courses/list/', views.listCourses, name='listCourses'),
    path('courses/<int:courses_id>/', views.courseDetail, name='courseDetail'),
    path('courses/<int:courses_id>/attendance', views.attendance, name='attendance'),
    path('courses/<int:courses_id>/attendance/confirm', views.confirmAttendance, name='confirmAttendance'),
]
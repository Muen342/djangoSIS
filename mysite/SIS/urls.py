from django.urls import path

from . import views

app_name = 'SIS'
urlpatterns = [
    path('', views.index, name='index'),
    path('students/', views.studentIndex, name='studentIndex'),
    path('students/list/<int:student_id>/', views.detail, name='detail'),
    path('students/list/<int:student_id>/courses', views.studentCourses, name='studentCourses'),
    path('students/list/<int:student_id>/courses/<int:course_id>', views.studentCourseDetail, name='studentCourseDetail'),
    path('students/list/<int:student_id>/edit', views.editStudent, name='editStudent'),
    path('students/list/<int:student_id>/confirmStudent/', views.confirmStudent, name='confirmStudent'),
    path('students/add/', views.addStudent, name='addStudent'),
    path('students/list/', views.listStudents, name='listStudents'),
    path('students/add/confirm', views.addStudentConfirm, name='addStudentConfirm'),
]
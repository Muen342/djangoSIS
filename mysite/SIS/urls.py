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
    path('courses/', views.coursesIndex, name='coursesIndex'),
    path('courses/list/', views.listCourses, name='listCourses'),
    path('courses/<int:courses_id>/', views.courseDetail, name='courseDetail'),
    path('courses/<int:courses_id>/attendance', views.attendance, name='attendance'),
    path('courses/<int:courses_id>/attendance/confirm', views.confirmAttendance, name='confirmAttendance'),
    path('locker/', views.lockerIndex, name='lockerIndex'),
    path('locker/add/', views.addLocker, name='addLocker'),
    path('locker/list/', views.listLocker, name='listLocker'),
    path('locker/<int:locker_id>', views.lockerDetail, name='lockerDetail'),
    path('locker/list/<int:locker_id>/edit', views.editLocker, name='editLocker'),
    path('locker/list/<int:locker_id>/confirmLocker', views.confirmLocker, name='confirmLocker'),
    path('locker/add/confirm', views.addLockerConfirm, name='addLockerConfirm'),
]
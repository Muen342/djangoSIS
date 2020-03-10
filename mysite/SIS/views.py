from django.shortcuts import render
from django.template import loader
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from .models import Student, Locker, Teacher, Courses, Assignment, Marks, Attendance
from django.views import generic
import datetime

def index(request):
    return render(request, 'homepage/index.html',context=None)

def studentIndex(request):
    student_list = Student.objects.all()
    template = loader.get_template('students/index.html')
    context = {
        'student_list': student_list,
    }
    return HttpResponse(template.render(context, request))

def addStudent(request):
    return render(request, 'students/addStudent.html',context=None)

def listStudents(request):
    student_list = Student.objects.all()
    template = loader.get_template('students/studentList.html')
    context = {
        'student_list': student_list,
    }
    return HttpResponse(template.render(context, request))

def detail(request, student_id):
    try:
        student = Student.objects.get(pk=student_id)
    except Student.DoesNotExist:
        raise Http404("Student does not exist")
    return render(request, 'students/detail.html', {'student': student})

def editStudent(request, student_id):
    try:
        student = Student.objects.get(pk=student_id)
    except Student.DoesNotExist:
        raise Http404("Student does not exist")
    return render(request, 'students/editStudent.html', {'student': student})

def confirmStudent(request, student_id):
    try:
        student = Student.objects.get(pk=student_id)
    except Student.DoesNotExist:
        raise Http404("Student does not exist")
    else:
        if(request.POST['id'] == '' or request.POST['fname'] == '' or request.POST['lname'] == '' or request.POST['grade'] == ''):
            return render(request, 'students/editStudent.html', {
            'student': student,
            'error_message': "One of your fields are empty",
            })
        else:
            d = Student.objects.get(pk=student.id)
            d.delete()
            s = Student(id=request.POST['id'], grade=request.POST['grade'], name=request.POST['fname'], surname=request.POST['lname'],locker_id=student.locker_id)
            s.save()
            return HttpResponseRedirect(reverse('SIS:detail', args=(request.POST['id'],)))

def addStudentConfirm(request):
    if(request.POST['id'] == '' or request.POST['fname'] == '' or request.POST['lname'] == '' or request.POST['grade'] == ''):
            return render(request, 'students/addStudent.html', {
            'error_message': "One of your fields are empty",
            })
    else:
        try:
            student = Student.objects.get(pk=request.POST['id'])
            if(student.id > 0):
                return render(request, 'students/addStudent.html', {
                'error_message': "This student already exists",
                })
        except Student.DoesNotExist:
            try:
                locker = Locker.objects.get(pk=request.POST['locker'])
                if(locker.id >= 0):
                    s = Student(id=request.POST['id'], grade=request.POST['grade'], name=request.POST['fname'], surname=request.POST['lname'],locker_id=request.POST['locker'])
                    s.save()
                    return render(request, 'students/addStudent.html', {
                    'error_message': "Successfully added",
                    })
            except Locker.DoesNotExist:
                return render(request, 'students/addStudent.html', {
                'error_message': "The locker doesn't exist, please create one first",
                })
                
def coursesIndex(request):
    courses_list = Courses.objects.all()
    template = loader.get_template('courses/index.html')
    context = {
        'courses_list': courses_list,
    }
    return HttpResponse(template.render(context, request))

def listCourses(request):
    courses_list = Courses.objects.all()
    template = loader.get_template('courses/listCourses.html')
    context = {
        'courses_list': courses_list,
    }
    return HttpResponse(template.render(context, request))

def courseDetail(request, courses_id):
    try:
        course = Courses.objects.get(pk=courses_id)
    except Courses.DoesNotExist:
        raise Http404("Course does not exist")
    return render(request, 'courses/courseDetail.html', {'course': course})

def attendance(request, courses_id):
    try:
        course = Courses.objects.get(pk=courses_id)
    except Courses.DoesNotExist:
        raise Http404("Course does not exist")
    students = course.students.split(", ")
    student_list = []
    for stud in students:
        try:
            s = Student.objects.get(pk=int(stud))
        except Student.DoesNotExist:
            raise Http404("Student does not exist")
        student_list.append(s)
    return render(request, 'courses/attendance.html', {
        'course': course,
        'student_list': student_list,
    })

def confirmAttendance(request, courses_id):
    try:
        course = Courses.objects.get(pk=courses_id)
    except Courses.DoesNotExist:
        raise Http404("Course does not exist")
    students = course.students.split(", ")
    for stud in students:
        att = Attendance.objects.filter(course_id=courses_id, student_id=stud, date__gte=datetime.date.today())
        if att: 
            if att[0].attendance != request.POST[stud]:
                att[0].attendance = request.POST[stud]
        else:
            a = Attendance(attendance=request.POST[stud], course_id=courses_id, student_id=stud)
            a.save()
    return HttpResponseRedirect(reverse('SIS:courseDetail', args=(courses_id,)))
from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from .models import Student, Locker, Teacher, Courses, Assignment, Marks
from django.views import generic

def studentIndex(request):
    student_list = Student.objects.all()
    template = loader.get_template('students/index.html')
    context = {
        'student_list': student_list,
    }
    return HttpResponse(template.render(context, request))
def index(request):
    return render(request, 'homepage/index.html',context=None)

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
def studentCourses(request, student_id):
    # course_list = Courses.objects.raw("Select * from SIS_courses where students like '%" + str(student_id) + "%'")
    course_list = Courses.objects.all()
    return render(request, 'students/studentCourses.html', {'course_list': course_list, 'student_id': student_id})

def studentCourseDetail(request, student_id, course_id):
    try:
        course = Courses.objects.get(pk=course_id)
        
    except Student.DoesNotExist:
        raise Http404("Course does not exist")
    else:
        return render(request, 'students/studentCourseDetail.html', {'student_id':student_id, 'course': course})
from django.shortcuts import render
from django.template import loader
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from .models import Student, Locker, Teacher, Courses, Assignment, Marks, Attendance
from django.views import generic
from django.db import connection
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
def studentCourses(request, student_id):
    course_list = Courses.objects.filter(students__contains=("*" + str(student_id)) + "*" )
    #course_list = Courses.objects.all()
    return render(request, 'students/studentCourses.html', {'course_list': course_list, 'student_id': student_id})

def studentCourseDetail(request, student_id, course_id):
    try:
        course = Courses.objects.get(pk=course_id)
        teacher = Teacher.objects.get(pk=course.teacher_id)
        assignment_list = Assignment.objects.raw("Select * from sis_assignment where course_id = '" + str(course_id) + "';")
        for assignment in assignment_list:
            mark = Marks.objects.raw("Select * from sis_marks where student_id = '" + str(student_id) + "' and assignment_id = '" + str(assignment.id) + "' and id > 0;")
            assignment.mark = mark[0].mark
    except Student.DoesNotExist:
        raise Http404("Course does not exist")
    else:
        return render(request, 'students/studentCourseDetail.html', {'student_id':student_id, 'course': course, 'teacher':teacher, 'assignment_list':assignment_list})
                
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
            s = Student.objects.get(pk=int(stud[1:-1]))
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
        att = Attendance.objects.filter(course_id=courses_id, student_id=stud[1:-1], date__gte=datetime.date.today())
        if att: 
            if att[0].attendance != request.POST[stud[1:-1]]:
                att[0].attendance = request.POST[stud[1:-1]]
<<<<<<< HEAD
                att[0].save()
=======
>>>>>>> hotfix
        else:
            a = Attendance(attendance=request.POST[stud[1:-1]], course_id=courses_id, student_id=stud[1:-1])
            a.save()
    return HttpResponseRedirect(reverse('SIS:courseDetail', args=(courses_id,)))

def viewAttendance(request, courses_id):
    try:
        course = Courses.objects.get(pk=courses_id)
    except Courses.DoesNotExist:
        raise Http404("Course does not exist")

    students = course.students.split(", ")
    att = Attendance.objects.filter(course_id=courses_id)
    attendance_list = []
    date_list = []
    for stud in students:
        try:
            s = Student.objects.get(pk=int(stud[1:-1]))
        except Student.DoesNotExist:
            raise Http404("Student does not exist")
        attendance_list.append({'id': s.id, 'name': s.surname + ", " + s.name})
    
    if att:
        date_list = att.values('date').order_by('date').distinct()

    if date_list:
        for stud in attendance_list:
            stud['attendance'] = []
            for d in date_list:
                p = att.filter(student_id=stud['id'], date=d['date'])
                if p:
                    stud['attendance'].append(p[0].attendance)
                else:
                    stud['atendance'].append('?')

    return render(request, 'courses/viewAttendance.html', {
        'course': course,
        'attendance_list': attendance_list,
        'date_list': date_list,
        })

def lockerIndex(request):
    locker_list = Locker.objects.all()
    template = loader.get_template('Locker/index.html')
    context = {
        'locker_list': locker_list,
    }
    return HttpResponse(template.render(context, request))

def lockerDetail(request, locker_id):
    try:
        locker = Locker.objects.get(pk=locker_id)
    except Locker.DoesNotExist:
        raise Http404("locker does not exist")
    return render(request, 'Locker/detail.html', {'locker': locker})

def addLocker(request):
    return render(request, 'Locker/addLocker.html',context=None)

def listLocker(request):
    locker_list = Locker.objects.all()
    template = loader.get_template('Locker/lockerList.html')
    context = {
        'locker_list': locker_list,
    }
    return HttpResponse(template.render(context, request))

def editLocker(request, locker_id):
    try:
        locker = Locker.objects.get(pk=locker_id)
    except Locker.DoesNotExist:
        raise Http404("Locker does not exist")
    return render(request, 'Locker/editLocker.html', {'locker': locker})

def confirmLocker(request, locker_id):
    try:
        locker = Locker.objects.get(pk=locker_id)
    except Locker.DoesNotExist:
        raise Http404("Locker does not exist")
    else:
        if(request.POST['id'] == '' or request.POST['location'] == '' or request.POST['combination'] == '' or request.POST['active'] == ''):
            return render(request, 'Locker/editLocker.html', {
            'locker': locker,
            'error_message': "One of your fields are empty",
            })
        else:
            d = Locker.objects.get(pk=locker.id)
            d.delete()
            s = Locker(id=request.POST['id'], location=request.POST['location'], combination=request.POST['combination'], active=request.POST['active'])
            s.save()
            return HttpResponseRedirect(reverse('SIS:lockerDetail', args=(request.POST['id'],)))
def addLockerConfirm(request):
    if(request.POST['id'] == '' or request.POST['location'] == '' or request.POST['combination'] == '' or request.POST['active'] == ''):
            return render(request, 'Locker/addLocker.html', {
            'error_message': "One of your fields are empty",
            })
    else:
        try:
            locker = Locker.objects.get(pk=request.POST['id'])
            if(locker.id > 0):
                return render(request, 'Locker/addLocker.html', {
                'error_message': "This locker id already exists",
                })
        except Locker.DoesNotExist:
            s = Locker(id=request.POST['id'], location=request.POST['location'], combination=request.POST['combination'], active=request.POST['active'])
            s.save()
            return render(request, 'Locker/addLocker.html', {
            'error_message': "Successfully added",
            })

def login(request):
    return render(request, 'login/login.html',context=None)
def dictfetchall(cursor): 
    "Returns all rows from a cursor as a dict" 
    desc = cursor.description 
    return [
            dict(zip([col[0] for col in desc], row)) 
            for row in cursor.fetchall() 
    ]
def loginConfirm(request):
    with connection.cursor() as cursor:
        cursor.execute("Select type from system_users where user_id = '" + str(request.POST['id']) + "' and user_pw = '" + str(request.POST['password']) + "'")
        result = dictfetchall(cursor)
    if(len(result) == 0):
        return render(request, 'login/login.html', {
        'error_message': "Login failed",
        })
    else:
        request.session['user_type'] = result[0]['type']
        request.session['logged_in'] = 1
        print(request.session['user_type'])
        return render(request, 'homepage/index.html')
    
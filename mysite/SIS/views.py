from django.shortcuts import render
from django.template import loader, RequestContext
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from .models import Student, Locker, Teacher, Courses, Assignment, Marks, Attendance, User, Permissions
from django.views import generic
from django.db import connection
import datetime

def index(request):
    permissions = request.session['user_permissions']
    return render(request, 'homepage/index.html',{'permissions':permissions})

# Student views
def studentIndex(request):
    permissions = request.session['user_permissions']
    student_list = Student.objects.all()
    template = loader.get_template('students/index.html')
    context = {
        'student_list': student_list,
        'permissions':permissions,
    }
    return HttpResponse(template.render(context, request))

def addStudent(request):
    permissions = request.session['user_permissions']
    locker_list = Locker.objects.all()
    return render(request, 'students/addStudent.html',{'locker_list':locker_list,'permissions':permissions})

def listStudents(request):
    permissions = request.session['user_permissions']
    student_list = Student.objects.all()
    template = loader.get_template('students/studentList.html')
    context = {
        'student_list': student_list,
        'permissions':permissions,
    }
    return HttpResponse(template.render(context, request))

def detail(request, student_id):
    permissions = request.session['user_permissions']
    try:
        student = Student.objects.get(pk=student_id)
    except Student.DoesNotExist:
        raise Http404("Student does not exist")
    return render(request, 'students/detail.html', {'student': student,'permissions':permissions})

def editStudent(request, student_id):
    permissions = request.session['user_permissions']
    locker_list = Locker.objects.all()
    try:
        student = Student.objects.get(pk=student_id)
        currlock = Locker.objects.get(pk=student.locker_id)
    except Student.DoesNotExist:
        raise Http404("Student does not exist")
    return render(request, 'students/editStudent.html', {'student': student, 'currlock': currlock,'locker_list': locker_list,'permissions':permissions})

def confirmStudent(request, student_id):
    permissions = request.session['user_permissions']
    try:
        student = Student.objects.get(pk=student_id)
    except Student.DoesNotExist:
        raise Http404("Student does not exist")
    else:
        if(request.POST['id'] == '' or request.POST['fname'] == '' or request.POST['lname'] == '' or request.POST['grade'] == ''):
            return render(request, 'students/editStudent.html', {
            'student': student,
            'permissions':permissions,
            'error_message': "One of your fields are empty",
            })
        else:
            if(student.id != request.POST['id']):
                d = Student.objects.get(pk=student.id)
                d.delete()
                s = Student(id=request.POST['id'], grade=request.POST['grade'], name=request.POST['fname'], surname=request.POST['lname'],locker_id=request.POST['locker'])
                s.save()
            else:
                s = Student.objects.get(pk=student.id)
                s.grade = request.POST['grade']
                s.name = request.POST['fname']
                s.surname = request.POST['lname']
                s.locker_id = request.POST['locker']
                s.save()
            return HttpResponseRedirect(reverse('SIS:detail', args=(request.POST['id'],)))

def addStudentConfirm(request):
    permissions = request.session['user_permissions']
    if(request.POST['id'] == '' or request.POST['fname'] == '' or request.POST['lname'] == '' or request.POST['grade'] == ''):
            return render(request, 'students/addStudent.html', {
            'error_message': "One of your fields are empty",'permissions':permissions
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
                    'permissions':permissions
                    })
            except Locker.DoesNotExist:
                return render(request, 'students/addStudent.html', {
                'error_message': "The locker doesn't exist, please create one first",
                })

def studentCourses(request, student_id):
    permissions = request.session['user_permissions']
    course_list = Courses.objects.filter(students__contains=("*" + str(student_id)) + "*" )
    #course_list = Courses.objects.all()
    return render(request, 'students/studentCourses.html', {'course_list': course_list, 'student_id': student_id,'permissions':permissions})

def studentCourseDetail(request, student_id, course_id):
    permissions = request.session['user_permissions']
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
        return render(request, 'students/studentCourseDetail.html', {'student_id':student_id, 'course': course, 'teacher':teacher, 'assignment_list':assignment_list,'permissions':permissions})
                
# Course views
def coursesIndex(request):
    permissions = request.session['user_permissions']
    courses_list = Courses.objects.all()
    template = loader.get_template('courses/index.html')
    context = {
        'courses_list': courses_list,
        'permissions':permissions,
    }
    return HttpResponse(template.render(context, request))

def listCourses(request):
    permissions = request.session['user_permissions']
    courses_list = Courses.objects.all()
    template = loader.get_template('courses/listCourses.html')
    context = {
        'courses_list': courses_list,
        'permissions':permissions,
    }
    return HttpResponse(template.render(context, request))

def courseDetail(request, courses_id):
    permissions = request.session['user_permissions']
    try:
        course = Courses.objects.get(pk=courses_id)
    except Courses.DoesNotExist:
        raise Http404("Course does not exist")
    return render(request, 'courses/courseDetail.html', {'course': course,'permissions':permissions})

def attendance(request, courses_id):
    permissions = request.session['user_permissions']
    try:
        course = Courses.objects.get(pk=courses_id)
    except Courses.DoesNotExist:
        raise Http404("Course does not exist")
    students = course.students.split(", ")
    student_list = []
    for stud in students:
        if stud != '':
            try:
                s = Student.objects.get(pk=int(stud[1:-1]))
            except Student.DoesNotExist:
                raise Http404("Student does not exist")
            student_list.append(s)
    return render(request, 'courses/attendance.html', {
        'course': course,
        'student_list': student_list,
        'permissions':permissions,
    })

def confirmAttendance(request, courses_id):
    permissions = request.session['user_permissions']
    try:
        course = Courses.objects.get(pk=courses_id)
    except Courses.DoesNotExist:
        raise Http404("Course does not exist")

    students = course.students.split(", ")
    student_list = []
    for stud in students:
        if stud != '':
            try:
                s = Student.objects.get(pk=int(stud[1:-1]))
            except Student.DoesNotExist:
                raise Http404("Student does not exist")
            student_list.append(s)

    for stud in students:
        if request.POST[stud[1:-1]] == '':
            return render(request, 'courses/attendance.html', {
                    'error_message': "One of your fields is empty",
                    'course': course,
                    'student_list': student_list
                    })
        if request.POST[stud[1:-1]] not in ['A', 'E', 'P']:
            return render(request, 'courses/attendance.html', {
                    'error_message': "Please only enter valid values",
                    'course': course,
                    'student_list': student_list
                    })
        att = Attendance.objects.filter(course_id=courses_id, student_id=stud[1:-1], date__gte=datetime.date.today())
        if att: 
            if att[0].attendance != request.POST[stud[1:-1]]:
                att[0].attendance = request.POST[stud[1:-1]]
                att[0].save()
        else:
            a = Attendance(attendance=request.POST[stud[1:-1]], course_id=courses_id, student_id=stud[1:-1])
            a.save()

    return HttpResponseRedirect(reverse('SIS:courseDetail', args=(courses_id,)))

def viewAttendance(request, courses_id):
    permissions = request.session['user_permissions']
    try:
        course = Courses.objects.get(pk=courses_id)
    except Courses.DoesNotExist:
        raise Http404("Course does not exist")

    students = course.students.split(", ")
    att = Attendance.objects.filter(course_id=courses_id)
    attendance_list = []
    date_list = []
    for stud in students:
        if stud != '':
            try:
                s = Student.objects.get(pk=int(stud[1:-1]))
            except Student.DoesNotExist:
                raise Http404("Student does not exist")
            attendance_list.append({'id': s.id, 'name': s.surname + ", " + s.name})
    
    if attendance_list:
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
        'permissions':permissions,
        'date_list': date_list,
        })

def editCourse(request, courses_id):
    permissions = request.session['user_permissions']
    try:
        course = Courses.objects.get(pk=courses_id)
    except Courses.DoesNotExist:
        raise Http404("Course does not exist")
    teacher_list = Teacher.objects.all()
    return render(request, 'courses/editCourse.html', {'course': course, 'teacher_list': teacher_list,'permissions':permissions})

def editCourseConfirm(request, courses_id):
    try:
        course = Courses.objects.get(pk=courses_id)
    except Courses.DoesNotExist:
        raise Http404("Course does not exist")

    if request.POST["code"] == '' or request.POST["title"] == '' or request.POST["credit"] == '' or request.POST["description"] == '':
        return render(request, 'courses/editCourse.html', {
                    'error_message': "One of your fields are empty",
                    'course': course
                    })
    if not (request.POST["credit"].replace('.','',1).isdigit()):
        return render(request, 'courses/editCourse.html', {
                    'error_message': "The credit value must be a number",
                    'course': course
                    })
    
    try:
        t = Teacher.objects.get(pk=request.POST["teacher"])
    except Teacher.DoesNotExist:
        return render(request, 'courses/editCourse.html', {
                    'error_message': "Teacher does not exist",
                    'course': course
                    })

    course.code = request.POST["code"]
    course.title = request.POST["title"]
    course.credit = request.POST["credit"]
    course.description = request.POST["description"]
    course.teacher_id = request.POST["teacher"]
    course.save()

    return HttpResponseRedirect(reverse('SIS:courseDetail', args=(courses_id,)))

def addCourse(request):
    permissions = request.session['user_permissions']
    teacher_list = Teacher.objects.all()
    return render(request, 'courses/addCourse.html', {'teacher_list': teacher_list,'permissions':permissions})

def addCourseConfirm(request):
    permissions = request.session['user_permissions']
    if request.POST["code"] == '' or request.POST["title"] == '' or request.POST["credit"] == '' or request.POST["description"] == '':
        return render(request, 'courses/addCourse.html', {
                    'error_message': "One of your fields are empty",
                    'permissions':permissions,
                    })
    if not (request.POST["credit"].replace('.','',1).isdigit()):
        return render(request, 'courses/addCourse.html', {
                    'error_message': "The credit value must be a number",
                    })

    try:
        t = Teacher.objects.get(pk=request.POST["teacher"])
    except Teacher.DoesNotExist:
        return render(request, 'courses/addCourse.html', {
                    'error_message': "Teacher does not exist",
                    'permissions':permissions,
                    })
    
    course = Courses(code=request.POST["code"], title=request.POST["title"], credit=request.POST["credit"], description=request.POST["description"], teacher_id=request.POST["teacher"])
    course.save()
    
    return HttpResponseRedirect(reverse('SIS:courseDetail', args=(course.id,)))

def classList(request, courses_id):
    permissions = request.session['user_permissions']
    try:
        course = Courses.objects.get(pk=courses_id)
    except Courses.DoesNotExist:
        raise Http404("Course does not exist")
    students = course.students.split(", ")
    student_list = []
    for stud in students:
        if stud != '':
            try:
                s = Student.objects.get(pk=int(stud[1:-1]))
            except Student.DoesNotExist:
                raise Http404("Student does not exist")
            student_list.append(s)
    return render(request, 'courses/classList.html', {
        'course': course,
        'permissions':permissions,
        'student_list': student_list,
    })

# Locker views
def lockerIndex(request):
    permissions = request.session['user_permissions']
    locker_list = Locker.objects.all()
    template = loader.get_template('Locker/index.html')
    context = {
        'locker_list': locker_list,
        'permissions':permissions,
    }
    return HttpResponse(template.render(context, request))

def lockerDetail(request, locker_id):
    permissions = request.session['user_permissions']
    try:
        locker = Locker.objects.get(pk=locker_id)
    except Locker.DoesNotExist:
        raise Http404("locker does not exist")
    return render(request, 'Locker/detail.html', {'locker': locker,'permissions':permissions})

def addLocker(request):
    permissions = request.session['user_permissions']
    return render(request, 'Locker/addLocker.html',{'permissions':permissions})

def listLocker(request):
    permissions = request.session['user_permissions']
    locker_list = Locker.objects.all()
    template = loader.get_template('Locker/lockerList.html')
    context = {
        'locker_list': locker_list,
        'permissions':permissions,
    }
    return HttpResponse(template.render(context, request))

def editLocker(request, locker_id):
    permissions = request.session['user_permissions']
    try:
        locker = Locker.objects.get(pk=locker_id)
    except Locker.DoesNotExist:
        raise Http404("Locker does not exist")
    return render(request, 'Locker/editLocker.html', {'locker': locker,'permissions':permissions})

def confirmLocker(request, locker_id):
    permissions = request.session['user_permissions']
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
            if(locker_id != locker.id):
                d = Locker.objects.get(pk=locker.id)
                d.delete()
                s = Locker(id=request.POST['id'], location=request.POST['location'], combination=request.POST['combination'], active=request.POST['active'])
                s.save()
            else:
                s = Locker.objects.get(pk=locker.id)
                s.location = request.POST['location']
                s.combination = request.POST['combination']
                s.active = request.POST['active']
                s.save()
            return HttpResponseRedirect(reverse('SIS:lockerDetail', args=(request.POST['id'],)))
def addLockerConfirm(request):
    permissions = request.session['user_permissions']
    if(request.POST['id'] == '' or request.POST['location'] == '' or request.POST['combination'] == '' or request.POST['active'] == ''):
            return render(request, 'Locker/addLocker.html', {
            'error_message': "One of your fields are empty",
            'permissions':permissions,
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
            'permissions':permissions,
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
    try:
        user = User.objects.get(pk=request.POST['id'])
    except:
        return render(request, 'login/login.html', {
        'error_message': "User ID not found",
        })
    if(user.user_pw == request.POST['password']):
        request.session['user_id'] = user.user_id
        request.session['user_type'] = user.user_type
        request.session['user_permissions'] = user.user_permissions
        return render(request, 'homepage/index.html', {'permissions':user.user_permissions})
        
    else:
        return render(request, 'login/login.html', {
        'error_message': "Incorrect Password",
        })

def usersIndex(request):
    permissions = request.session['user_permissions']
    return render(request, 'users/index.html',{'permissions':permissions})

def addUser(request):
    permissions = request.session['user_permissions']
    type_list = []
    for i in User.TYPES:
        type_list.append(i[0])
    return render(request, 'users/addUser.html',{'type_list':type_list,'permissions':permissions})

def listUsers(request):
    permissions = request.session['user_permissions']
    user_list = User.objects.all()
    template = loader.get_template('users/listUser.html')
    context = {
        'user_list': user_list,
        'permissions':permissions,
    }
    return HttpResponse(template.render(context, request))

def addUserConfirm(request):
    permissions = request.session['user_permissions']
    if(request.POST['id'] == '' or request.POST['password'] == '' or request.POST['type'] == ''):
            return render(request, 'users/addUser.html', {
            'error_message': "One of your fields are empty",
            'permissions':permissions,
            })
    else:
        try:
            user = User.objects.get(pk=request.POST['id'])
            if(len(user.user_id) > 0):
                return render(request, 'users/addUser.html', {
                'error_message': "This locker id already exists",
                'permissions':permissions,
                })
        except User.DoesNotExist:
            s = User(user_id=request.POST['id'], user_pw=request.POST['password'], user_type=request.POST['type'], user_permissions = '')
            s.save()
            return render(request, 'users/addUser.html', {
            'error_message': "Successfully added",
            'permissions':permissions,
            })

def userDetail(request, user_id):
    permission = request.session['user_permissions']
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        raise Http404("user does not exist")
    permissions = user.user_permissions[1:-1]
    permissions_list = permissions.split("**")
    return render(request, 'users/detail.html', {'user': user, 'permissions_list':permissions_list,'permissions':permission})

def changePermissions(request, user_id):
    permissions = request.session['user_permissions']
    listarr = Permissions.objects.all()
    listarr2 = listarr[0].permissions_list[1:-1]
    permission_list = listarr2.split("**")
    user = User.objects.get(pk=user_id)
    return render(request, 'users/changePermissions.html', {'user': user, 'permission_list':permission_list,'permissions':permissions})

def confirmPermissions(request, user_id):
    user = User.objects.get(pk=user_id)
    listarr = Permissions.objects.all()
    listarr2 = listarr[0].permissions_list[1:-1]
    permission_list = listarr2.split("**")
    for i in permission_list:
        try:
            if(request.POST[i]):
                if(user.user_permissions.find(i) == -1):
                    user.user_permissions = user.user_permissions + "*" + i + "*"
        except:
            perm = '*' + i + '*'
            index = user.user_permissions.find(perm)
            if(index != -1):
                user.user_permissions = user.user_permissions[:index] + user.user_permissions[index + len(perm):]
    user.save()
    if(user_id == request.session['user_id']):
        request.session['user_permissions'] = user.user_permissions
    permissions = request.session['user_permissions']
    return render(request, 'users/changePermissions.html', {'user': user, 'permission_list':permission_list,'permissions':permissions})
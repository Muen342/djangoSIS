from django import forms
from .models import Student, Permissions, Locker, Teacher, Courses, Assignment, Marks, Attendance, User


class PermissionForm(forms.Form):
    from .models import Permissions
    lists = Permissions.objects.all()
    liststr = lists[0].permissions_list
    liststr = liststr[1:-1]
    listarr = liststr.split("**")
    OPTIONS = listarr
    Permissions = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=OPTIONS)
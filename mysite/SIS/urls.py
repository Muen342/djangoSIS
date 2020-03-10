from django.urls import path

from . import views

app_name = 'SIS'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:student_id>/', views.detail, name='detail'),
    path('<int:student_id>/edit', views.editStudent, name='editStudent'),
    path('<int:student_id>/confirmStudent/', views.confirmStudent, name='confirmStudent'),
]
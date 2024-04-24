from django.urls import path
from .views import student_attendance, teacher_attendance, take_attendance, create_attendance, delete_attendance

app_name = 'attendance'

urlpatterns = [
    path('student/', student_attendance, name='student_attendance_page'),
    path('teacher/', teacher_attendance, name='teacher_attendance_page'),
    path('teacher/<int:group_id>/', take_attendance, name='take_attendance'),
    path('create_attendance/', create_attendance, name='create_attendance'),
]

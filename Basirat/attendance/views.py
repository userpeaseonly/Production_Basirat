from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from main.models import Group, Student
from .models import Attendance, AttendanceStudent
# from Basirat.main.models import Student, Group
import json
from django.db.models import F


@login_required(login_url='authentication:login')
@user_passes_test(lambda u: u.is_active)
def student_attendance(request):
    student = request.user
    group = student.student.group
    attendances = AttendanceStudent.objects.filter(attendance__group=group, student=student.student).annotate(
        date=F('attendance__date')).values('date', 'present')
    context = {
        'student': student,
        'attendances': attendances
    }
    return render(request, 'attendance/student_attendance.html', context)


@login_required(login_url='authentication:login')
@user_passes_test(lambda u: u.is_staff)
def teacher_attendance(request):
    groups = Group.objects.all()
    is_taken = {}
    for group in groups:
        is_taken[group] = Attendance.objects.filter(group=group, date=datetime.now().date()).exists()
    context = {
        'groups': groups,
        'is_taken': is_taken
    }
    return render(request, 'attendance/teacher_attendance.html', context)


@login_required(login_url='authentication:login')
@user_passes_test(lambda u: u.is_staff)
def take_attendance(request, group_id):
    group = Group.objects.get(id=group_id)
    context = {
        'group': group,
        'students': group.student_set.all(),
        'date': datetime.now().date()
    }
    return render(request, 'attendance/take_attendance.html', context)


@csrf_exempt
def create_attendance(request):
    if request.method == 'POST':
        group_id = request.POST.get('group_id')
        group = Group.objects.get(id=group_id)
        attendance, created = Attendance.objects.get_or_create(group=group, date=datetime.now().date())
        student_attendance_data = json.loads(request.POST.get('student_attendance'))
        for student_id, attendance_status in student_attendance_data.items():
            student = Student.objects.get(user=User.objects.get(id=int(student_id.split('_')[1])))
            present = True if attendance_status == 'present' else False
            AttendanceStudent.objects.update_or_create(attendance=attendance, student=student,
                                                       defaults={'present': present})
        return JsonResponse({'message': 'Attendance created successfully'})
    return JsonResponse({'error': 'Method not allowed'}, status=405)


def delete_attendance(request):
    return None

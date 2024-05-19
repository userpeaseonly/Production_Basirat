from django.contrib.auth.decorators import login_required
from django.db.models import F, Sum
from django.shortcuts import render

from attendance.models import AttendanceStudent
from django.utils import timezone
from notifications.models import Message
from tests.models import TestResult, ClosedQuestionResult


@login_required(login_url='authentication:login')
def home(request):
    the_student = request.user
    messages = Message.objects.all() if the_student.is_staff else Message.objects.filter(group=the_student.student.group)
    try:
        percentage_of_attendance = attendance(request).__round__(2)
        percentage_of_progress = calculate_progress(request).__round__(2)
    except Exception:
        percentage_of_attendance = all_attendance(request).__round__(2)
        percentage_of_progress = 0  # Set default progress if no data is available
    unchecked_tests = ClosedQuestionResult.objects.filter(is_correct=None)
    print(unchecked_tests)
    context = {
        'the_student': the_student,
        'percentage_of_attendance': percentage_of_attendance,
        'percentage_of_progress': percentage_of_progress,
        'unchecked_tests': unchecked_tests,
        'messages': messages
    }
    return render(request, 'main/home.html', context)


def attendance(request):
    student = request.user
    group = student.student.group
    try:
        attendance_student_filtered = AttendanceStudent.objects.filter(attendance__group=group,
                                                                       student=student.student).count() * 100
    except ZeroDivisionError:
        attendance_student_filtered = 1
    try:
        attendance_student = AttendanceStudent.objects.filter(attendance__group=group, student=student.student).count()
    except ZeroDivisionError:
        attendance_student = 1
    percentage_of_attendance = attendance_student / attendance_student_filtered
    return percentage_of_attendance


def all_attendance(request):
    try:
        attendance_students = AttendanceStudent.objects.filter(
            present=True).count() / AttendanceStudent.objects.all().count() * 100
    except ZeroDivisionError:
        attendance_students = 1
    return attendance_students


def calculate_progress(request):
    student = request.user
    test_results = (
        TestResult.objects.filter(student=student)
        .aggregate(total_score=Sum('score'), total_points=Sum('test__questions__points'))
    )
    if test_results['total_points'] > 0:
        percentage_of_progress = (test_results['total_score'] / test_results['total_points']) * 100
    else:
        percentage_of_progress = 0
    print(percentage_of_progress)
    return percentage_of_progress

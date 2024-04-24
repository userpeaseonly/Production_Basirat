from django.db import models

from main.models import Group, Student


class Attendance(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True, unique_for_date=True)

    def __str__(self):
        return self.group.group_number + ' ' + str(self.date)


class AttendanceStudent(models.Model):
    attendance = models.ForeignKey(Attendance, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    present = models.BooleanField(default=False)

    def __str__(self):
        return self.student.user.username

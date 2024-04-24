from django.db import models
from django.contrib.auth.models import User


class Group(models.Model):
    group_number = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.group_number


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    age = models.IntegerField()
    image = models.ImageField(upload_to='profile_pics', default='default.jpg')

    def __str__(self):
        return self.user.username


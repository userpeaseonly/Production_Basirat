from django.db import models
from main.models import Group
from django.contrib.auth.models import User


class Test(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    duration_minutes = models.IntegerField(default=60)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    groups = models.ManyToManyField(Group, related_name='tests')
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class Question(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    text = models.TextField(max_length=300)
    image = models.ImageField(upload_to='question_images', blank=True, null=True)
    explanation = models.TextField(blank=True, null=True)
    points = models.IntegerField(default=1)

    def get_correct_answer(self):
        try:
            correct_option = self.multiplechoiceoption_set.get(is_correct=True)
            return correct_option.choice
        except MultipleChoiceOption.DoesNotExist:
            return None

    def __str__(self):
        return self.text[:50]


class MultipleChoiceOption(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice = models.CharField(max_length=1, choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')])
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text[:50]


class TextAnswer(models.Model):
    question = models.OneToOneField(Question, on_delete=models.CASCADE, primary_key=True)
    expected_answer = models.TextField()

    def __str__(self):
        return self.expected_answer[:50]


class TestResult(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    score = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)
    time_taken = models.IntegerField()

    def __str__(self):
        return self.student.username + ' ' + self.test.title


class QuestionResult(models.Model):
    test_result = models.ForeignKey(TestResult, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    student_answer = models.CharField(max_length=1, choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')])
    is_correct = models.BooleanField()

    def __str__(self):
        return self.question.text[:50]


class ClosedQuestionResult(models.Model):
    test_result = models.ForeignKey(TestResult, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    student_answer = models.TextField()
    teacher_comment = models.TextField(blank=True, null=True)
    is_correct = models.BooleanField(null=True, blank=True)

    def __str__(self):
        return self.question.text[:50]


class TestSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(blank=True, null=True)

    def duration(self):
        if self.end_time:
            return self.end_time - self.start_time
        else:
            return None

    def __str__(self):
        return self.user.username + ' ' + self.test.title

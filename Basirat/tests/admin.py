from django.contrib import admin
from .models import Test, Question, MultipleChoiceOption, TextAnswer, TestResult, TestSession, ClosedQuestionResult

admin.site.register(Test)
admin.site.register(Question)
admin.site.register(MultipleChoiceOption)
admin.site.register(TextAnswer)

admin.site.register(TestResult)
admin.site.register(TestSession)
admin.site.register(ClosedQuestionResult)
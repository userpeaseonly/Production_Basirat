from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from .models import Test, Question, MultipleChoiceOption, TextAnswer, TestResult, QuestionResult, TestSession, \
    ClosedQuestionResult
from .signals import test_started, test_submitted
from main.models import Group, Student
from .restrictions import restrict_test_access, restrict_test_access_if_taken


@login_required(login_url='authentication:login')
def test_list(request):
    is_admin = request.user.is_staff
    if is_admin:
        tests = Test.objects.all()
    else:
        # tests = Test.objects.filter(groups__in=request.user.student.group)
        student = get_object_or_404(Student, user=request.user)
        tests = Test.objects.filter(groups__in=[student.group], is_active=True, start_date__lte=timezone.now(),
                                    end_date__gte=timezone.now()).exclude(testresult__student=request.user)
    completed_tests = Test.objects.filter(testresult__student=request.user)
    context = {
        'is_admin': is_admin,
        'tests': tests,
        'completed_tests': completed_tests,
    }
    return render(request, 'tests/test_list.html', context)


@login_required(login_url='authentication:login')
@user_passes_test(lambda u: u.is_staff)
def create_test_page(request):
    groups = Group.objects.all()
    context = {
        'groups': groups
    }
    return render(request, 'tests/create_test_page.html', context)


@csrf_exempt
def create_question(request):
    if request.method == 'POST':
        test = Test.objects.get(id=request.POST.get('test'))
        points = request.POST.get('points')
        if request.POST.get('points') == '':
            points = 1
        question = Question.objects.create(
            test=test,
            text=request.POST.get('text'),
            image=request.FILES.get('image'),
            explanation=request.POST.get('explanation'),
            points=points,
        )
        if request.POST.get('isOpenQuestion') == 'false':
            TextAnswer.objects.create(
                question=question,
                expected_answer='expected answer'
            )
        else:
            MultipleChoiceOption.objects.create(
                question=question,
                choice='A',
                text=request.POST.get('optionA'),
                is_correct=True if request.POST.get('correctOptionA') == 'true' else False
            )
            MultipleChoiceOption.objects.create(
                question=question,
                choice='B',
                text=request.POST.get('optionB'),
                is_correct=True if request.POST.get('correctOptionB') == 'true' else False
            )
            MultipleChoiceOption.objects.create(
                question=question,
                choice='C',
                text=request.POST.get('optionC'),
                is_correct=True if request.POST.get('correctOptionC') == 'true' else False
            )
            MultipleChoiceOption.objects.create(
                question=question,
                choice='D',
                text=request.POST.get('optionD'),
                is_correct=True if request.POST.get('correctOptionD') == 'true' else False
            )
    return JsonResponse({'success': False})


@login_required(login_url='authentication:login')
@user_passes_test(lambda u: u.is_staff)
def edit_test_page(request, test_id):
    test = Test.objects.get(id=test_id)
    groups = Group.objects.all()
    questions = Question.objects.filter(test=test)
    context = {
        'test': test,
        'groups': groups,
        'questions': questions,
    }
    return render(request, 'tests/edit_test_page.html', context)


def create_test(request):
    if request.method == 'POST':
        test = Test.objects.create(
            title=request.POST.get('title'),
            description=request.POST.get('description'),
            duration_minutes=int(request.POST.get('duration')),
            teacher=request.user,
            is_active=True if request.POST.get('is_active') == 'true' else False,
            start_date=request.POST.get('start_date'),
            end_date=request.POST.get('end_date'),
        )
        groups = request.POST.getlist('groups[]')
        test.groups.set(groups)
        test.save()
    return JsonResponse({'success': False})


def edit_test(request):
    if request.method == 'POST':
        test = Test.objects.get(id=request.POST.get('test_id'))
        test.title = request.POST.get('title')
        test.description = request.POST.get('description')
        test.duration_minutes = int(request.POST.get('duration'))
        test.is_active = True if request.POST.get('is_active') == 'true' else False
        test.start_date = request.POST.get('start_date')
        test.end_date = request.POST.get('end_date')
        groups = request.POST.getlist('groups[]')
        test.groups.set(groups)
        test.save()
    return JsonResponse({'success': False})


@csrf_exempt
def delete_test(request):
    if request.method == 'POST':
        try:
            test = Test.objects.get(id=request.POST.get('test'))
            test.delete()
            return JsonResponse({'success': True})
        except Test.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Test does not exist'})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method'})


@csrf_exempt
def deactivate_test_endpoint(request):
    if request.method == 'POST':
        test_id = request.POST.get('test')
        # Logic to deactivate the test
        # For example:
        test = Test.objects.get(id=test_id)
        if test.is_active:
            test.is_active = False
            text = 'deactivated'
        else:
            test.is_active = True
            text = 'activated'
        test.save()
        return JsonResponse({'message': f'Test {text} successfully!'})
    else:
        return JsonResponse({'error': 'Invalid request!'}, status=400)


@csrf_exempt
def delete_question(request):
    if request.method == 'POST':
        test = request.POST.get('test')
        question = get_object_or_404(Question, id=request.POST.get('question_id'), test=test)
        question.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'error': 'Question ID is missing'})


@restrict_test_access_if_taken
@restrict_test_access
def take_test(request, test_id):
    test = Test.objects.get(id=test_id)
    # test_started.send(sender=None, user=request.user, test=test)
    test_session_exists = TestSession.objects.filter(user=request.user, test=test).exists()
    if not test_session_exists:
        test_started.send(sender=None, user=request.user, test=test)
    else:
        return redirect('tests:test_result', test_id=test_id)
    context = {
        'test': test
    }
    return render(request, 'tests/take_test.html', context)


def submit_answers(request, test_id):
    if request.method == 'POST':
        test = Test.objects.get(id=test_id)
        test_submitted.send(sender=None, user=request.user, test=test)
        result = TestResult.objects.get_or_create(
            student=request.user,
            test=test,
            score=0,
            date=timezone.now(),
            time_taken=0
        )
        for question in test.question_set.all():
            choice_id = request.POST.get(f'question_{question.id}')
            if choice_id is not None:
                try:
                    choice = MultipleChoiceOption.objects.get(id=choice_id)
                    question_result = QuestionResult.objects.create(
                        test_result=TestResult.objects.get(student=request.user, test=test),
                        question=question,
                        student_answer=choice.choice,
                        is_correct=choice.is_correct
                    )
                    question_result.save()
                except Exception:
                    closed_question = ClosedQuestionResult.objects.create(
                        test_result=TestResult.objects.get(student=request.user, test=test),
                        question=question,
                        student_answer=request.POST.get(f'question_{question.id}')
                    )
                    closed_question.save()
        score = QuestionResult.objects.filter(test_result__student=request.user, test_result__test=test,
                                              is_correct=True).count()
        result = TestResult.objects.update(
            score=score,
            time_taken=TestSession.objects.get(user=request.user, test=test).duration().seconds
        )
        return redirect('tests:test_result', test_id=test_id)  # Redirect to a success page
    else:
        return redirect('error_page')  # Redirect to an error page if the request method is not POST


def test_result(request, test_id):
    test = Test.objects.get(id=test_id)
    result = TestResult.objects.get(student=request.user, test=test)
    context = {
        'test': test,
        'result': result,
    }
    return render(request, 'tests/results_page.html', context)


# def check_test(request, unchecked_test_id):
#     closed_question = ClosedQuestionResult.objects.get(id=unchecked_test_id)
#     context = {
#         'closed_question': closed_question,
#     }
#     return render(request, 'tests/check_test.html', context)

def check_test(request, unchecked_test_id):
    if request.method == 'POST':
        # Handle form submission
        comment = request.POST.get('comment')
        is_correct = request.POST.get('is_correct')
        try:
            question = ClosedQuestionResult.objects.get(id=unchecked_test_id)
            question.teacher_comment = comment
            question.is_correct = is_correct == 'true'
            question.save()
            return redirect('main:home')  # Redirect to success page
        except ClosedQuestionResult.DoesNotExist:
            return redirect('error_page')  # Redirect to error page if question not found
    else:
        # Render the form
        try:
            closed_question = ClosedQuestionResult.objects.get(id=unchecked_test_id)
            context = {'closed_question': closed_question}
            return render(request, 'tests/check_test.html', context)
        except ClosedQuestionResult.DoesNotExist:
            return redirect('error_page')  # Redirect to error page if question not found
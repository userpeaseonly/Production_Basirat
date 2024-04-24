from django.http import Http404
from functools import wraps

from django.urls import reverse
from django.utils import timezone
from django.shortcuts import get_object_or_404, redirect
from .models import Test, TestResult
from main.models import Student


def restrict_test_access(view_func):
    @wraps(view_func)
    def wrapper(request, test_id, *args, **kwargs):
        try:
            # Get the current student based on the request user
            student = get_object_or_404(Student, user=request.user)

            # Get the current datetime
            now = timezone.now()

            # Retrieve the test and check if it meets the conditions
            test = Test.objects.get(
                id=test_id,
                is_active=True,
                groups=student.group,
                start_date__lte=now,
                end_date__gte=now
            )
        except Test.DoesNotExist:
            raise Http404("Test does not exist or is not accessible")

        # If the test meets the conditions, execute the view function
        return view_func(request, test_id, *args, **kwargs)

    return wrapper


def restrict_test_access_if_taken(view_func):
    @wraps(view_func)
    def wrapper(request, test_id, *args, **kwargs):
        test = Test.objects.get(id=test_id)
        test_result_exists = TestResult.objects.filter(student=request.user, test=test).exists()
        if test_result_exists:
            return redirect(reverse('tests:test_list'))  # Redirect to tests page if TestResult exists
        return view_func(request, test_id, *args, **kwargs)  # Otherwise, proceed with the original view function

    return wrapper

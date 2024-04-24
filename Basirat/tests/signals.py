from django.dispatch import Signal
from django.utils import timezone
from .models import TestSession

# Define custom signals
test_started = Signal()
test_submitted = Signal()


def start_timer(sender, user, test, **kwargs):
    # Start the timer when the test is started
    TestSession.objects.create(user=user, test=test, start_time=timezone.now())


def stop_timer(sender, user, test, **kwargs):
    # Stop the timer when the test is submitted
    test_session = TestSession.objects.get(user=user, test=test)
    test_session.end_time = timezone.now()
    test_session.save()


# Connect signals to functions
test_started.connect(start_timer, dispatch_uid='start_timer')
test_submitted.connect(stop_timer, dispatch_uid='stop_timer')

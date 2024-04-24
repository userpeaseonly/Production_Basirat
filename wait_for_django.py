import time
import os


def wait_for_django():
    """Waits for a file indicating Django is ready"""
    while not os.path.exists("/tmp/django_ready"):
        time.sleep(1)
    print("Django is ready, starting Daphne...")


if __name__ == "__main__":
    wait_for_django()
    # Replace with your original Daphne command
    os.system("daphne -b 0.0.0.0:8001 Basirat.asgi:application")

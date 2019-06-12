from celery import shared_task
from celery.exceptions import SoftTimeLimitExceeded

from store import processing


@shared_task()
def task_process_photos():
    try:
        processing.process_photos()
    except SoftTimeLimitExceeded:
        # Expected, do not log the exception
        pass

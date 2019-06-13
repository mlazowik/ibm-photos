from celery import Celery

from django.conf import settings

app = Celery('photos')

# Using a string here means the worker don't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# The `expires` option prevents buildup of tasks when workers are down.
app.conf.beat_schedule = {
    'Process photos': {
        'task': 'store.tasks.task_process_photos',
        'schedule': settings.PROCESS_PHOTOS_INTERVAL,
        'options': {
            'expires': 1
        }
    },
}

# To ensure that at most one task of each listed type is running at any given
# time we kill this tasks right before their next scheduled execution.
#
# This works, because this tasks save their intermediate results always.
# This means that the whole job can be effectively split across multiple
# executions.
app.conf.task_annotations = {
    'store.tasks.task_process_photos': {
        'soft_time_limit': settings.PROCESS_PHOTOS_INTERVAL - 2,
        'time_limit': settings.PROCESS_PHOTOS_INTERVAL - 1
    },
}

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

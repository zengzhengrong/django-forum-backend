from __future__ import absolute_import , unicode_literals
import platform
import os
from celery import Celery

if platform.system() == 'Windows':
    os.environ.setdefault('FORKED_BY_MULTIPROCESSING','1')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'forum_backend_project.settings')

app = Celery('forum_backend')

app.config_from_object('django.conf:settings',namespace='CELERY')

app.autodiscover_tasks()


app.conf.update(
    timezone = 'Asia/Shanghai'
)

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))

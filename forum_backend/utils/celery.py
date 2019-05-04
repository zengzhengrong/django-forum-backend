from __future__ import absolute_import, unicode_literals
from celery import Celery

import os
os.environ.setdefault('FORKED_BY_MULTIPROCESSING','1')

app = Celery('tasks',
             broker='redis://',
             backend='redis://',
             include=['utils.tasks'])

# Optional configuration, see the application user guide.
app.conf.update(
    result_expires=3600,
)

if __name__ == '__main__':
    app.start()
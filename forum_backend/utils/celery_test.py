from __future__ import absolute_import, unicode_literals
from utils.celery import app
import time

app.conf.update(
    task_routes = {
        'utils.celery_test.add': {'queue': 'hipri'},
    },
    timezone = 'Asia/Shanghai'
)

@app.task
def add(x,y):
    return x+y

@app.task
def mul(x,y):
    return x*y

@app.task
def xsum(numbers):
    return sum(numbers)

@app.task
def time_sleep(seconds):
    time.sleep(seconds)
    return 'timeout'

if __name__ == "__main__":
    time_sleep.delay(10)
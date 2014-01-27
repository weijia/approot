import sys
from celery_main import Celery
from extra_settings.init_settings import init_settings

init_settings()
print sys.path
app = Celery('tasks', broker='django://')

@app.task
def add(x, y):
    return x + y
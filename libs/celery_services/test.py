from extra_settings.init_settings import init_settings
init_settings()
from celery_main import Celery




app = Celery('tasks', broker='django://')

@app.task
def add(x, y):
    return x + y
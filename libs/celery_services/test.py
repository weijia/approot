import sys
sys.path.append("D:\\work\\mine\\codes\\ufs_django\\approot")
from extra_settings.init_settings import init_settings
init_settings()
from celery import Celery


#Ref: http://docs.celeryproject.org/en/master/django/first-steps-with-django.html
app = Celery('proj')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
#app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

@app.task
def add(x, y):
    return x + y
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
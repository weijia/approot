from celery import Celery
from puller import add_git_path_and_pull

app = Celery('tasks', broker='amqp://guest@localhost//')

@app.task
def pull(x, y):
    add_git_path_and_pull()
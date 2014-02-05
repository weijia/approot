from celery_main import app
from celery.execute import send_task    

res = send_task('libs.celery_services.test.add', [], {"x":1, "y":10})
print res.get()


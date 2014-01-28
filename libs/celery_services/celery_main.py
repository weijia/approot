from __future__ import absolute_import
import sys
sys.path.append("D:\\work\\mine\\codes\\ufs_django\\approot")
import configuration
from extra_settings.init_settings import init_settings
init_settings()
from celery import Celery

app = Celery('proj',
             broker='django://',
             include=['libs.celery_services.test'])

# Optional configuration, see the application user guide.
app.conf.update(
    CELERY_TASK_RESULT_EXPIRES=3600,
    CELERY_RESULT_BACKEND='djcelery.backends.database:DatabaseBackend',
)

if __name__ == '__main__':
    app.start()
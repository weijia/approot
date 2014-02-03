from __future__ import absolute_import
import sys
sys.path.append("D:\\work\\mine\\codes\\ufs_django\\approot")
import configuration
from extra_settings.init_settings import init_settings
init_settings()
from celery import Celery


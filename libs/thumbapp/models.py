# -*- coding: utf-8 -*-
from django.db import models
from ui_framework.objsys.models import UfsObj
from django.utils.translation import ugettext_lazy

# Create your models here.

############################################
class ThumbCache(models.Model):
    '''
    某个对象也有可能只有thumb没有obj？既然有thumb就给它创建一个obj，这样所有的终端上都能检索到所有的文件信息
    '''
    #obj_uuid = models.CharField (ugettext_lazy(u"Object UUID"), help_text=ugettext_lazy(u"Object UUID"), max_length=50, null=True, blank=True)
    thumb_full_path = models.TextField(ugettext_lazy(u"Thumbnail full path"), help_text=ugettext_lazy(u"Thumbnail full path"), null=True, blank=True)
    obj = models.ForeignKey(UfsObj, null=True, blank=True)
    timestamp = models.DateTimeField('date published', auto_now_add=True)
    
from django.db import models
from django.utils.translation import ugettext_lazy

# Create your models here.
class resource(models.Model):
    created = models.DateTimeField(ugettext_lazy(u'Date created'), auto_now_add=True)
    last_accessed = models.DateTimeField(ugettext_lazy(u'Date created'), auto_add=True)
    access_cnt = models.IntegerField(ugettext_lazy(u'Last accessed'))
    url = models.CharField(ugettext_lazy(u'Url'), max_length=1024)
    cached_path = models.CharField(ugettext_lazy(u'Cached path'), max_length=1024)
    
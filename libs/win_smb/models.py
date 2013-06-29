from django.db import models
from django.utils.translation import ugettext_lazy

# Create your models here.
class NetDriver(models.Model):
    created = models.DateTimeField(ugettext_lazy(u'Date created'), auto_now_add=True)
    last_accessed = models.DateTimeField(ugettext_lazy(u'Date created'), auto_now=True)
    access_cnt = models.IntegerField(ugettext_lazy(u'Last accessed'))
    remote = models.CharField(ugettext_lazy(u'Remote storage identifier'), max_length=1024)
    local = models.CharField(ugettext_lazy(u'Local storage identifier'), max_length=1024)
    def __unicode__(self):
        return self.local +": <- "+self.remote
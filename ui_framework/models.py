from django.db import models
from django.utils.translation import ugettext_lazy

# Create your models here.
class StaticFile(models.Model):
    path = models.CharField(ugettext_lazy(u'Path'), max_length=500, help_text = ugettext_lazy(u'Path'))
    cachable = models.BooleanField(ugettext_lazy(u'Cachable'), help_text = ugettext_lazy(u'If it is cachable'))
    def __unicode__(self):
        return unicode(self.path)

from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from objsys.models import UfsObj, get_new_uuid


class CollectionItem(models.Model):
    obj = models.ForeignKey(UfsObj)
    uuid = models.CharField(max_length=60, default=get_new_uuid)
    id_in_col = models.CharField(max_length=60)
    timestamp = models.DateTimeField('date published', auto_now_add=True)
    user = models.ForeignKey(User)

    def __unicode__(self):
        return unicode('collection:' + self.uuid + ' ' + self.obj.__unicode__() + '(' + self.id_in_col + ')')

    class Meta:
        permissions = (
            ('view_collection_item', 'Can view collection item'),
        )
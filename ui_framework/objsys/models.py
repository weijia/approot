from django.db import models
from django.contrib.auth.models import User
import uuid

try:
    import tagging

    tagging.register(UfsObj)
except:
    pass


def get_new_uuid():
    return str(uuid.uuid4())


# Create your models here.
class UfsObj(models.Model):
    full_path = models.TextField(null=True, blank=True)
    ufs_url = models.TextField(help_text='start with ufs:// or uuid:// etc.')
    uuid = models.CharField(max_length=60, default=get_new_uuid, help_text='the uuid string of the object, no "uuid" prefix needed')
    head_md5 = models.CharField(max_length=60, null=True, blank=True, help_text="the md5 for the header of the object")
	total_md5 = models.CharField(max_length=60, null=True, blank=True, help_text="the entire object's md5 hash value")
    timestamp = models.DateTimeField('date published', auto_now_add=True)
    size = models.BigIntegerField(null=True, blank=True)
    user = models.ForeignKey(User, null=True, blank=True)
    description = models.TextField(null=True, blank=True, help_text="JSON description for this object")
	valid = models.BooleanField(default=True, help_text="is this field valid")
	relations = models.ManyToManyField("self", related_name='relations', null=True, blank=True, help_text="Related other information objects")

    def __unicode__(self):
        return unicode(self.ufs_url + ' uuid:' + self.uuid)

    ####################
    # Only used in UFS
    def save(self, *args, **kwargs):
        import os

        if not (self.full_path is None):

            if os.path.exists(self.full_path) and (not (os.path.isdir(self.full_path))):
                try:
                    import libsys
                    import json
                    from libs.obj_related.local_obj import LocalObj

                    local_obj = LocalObj(self.full_path)

                    if self.size is None:
                        self.size = local_obj.get_size()

                    if self.description is None:
                        self.description = json.dumps({"magic_type": local_obj.get_type()})
                except IOError:
                    import traceback

                    traceback.print_exc()
            else:
                print 'is dir or not exist'
                pass
            #print 'full path is:', self.full_path, self.size, self.description, os.path.isdir(self.full_path)
        super(UfsObj, self).save(*args, **kwargs) # Call the "real" save() method.

    ####################
    def get_type(self):
        if not (self.full_path is None):
            import os

            if os.path.exists(self.full_path):
                import libsys

                try:
                    from libs.obj_related.local_obj import LocalObj
                    import json

                    if self.description is None:
                        local_obj = LocalObj(self.full_path)
                        magic_type = local_obj.get_type()
                        self.description = json.dumps({"magic_type": magic_type})
                    else:
                        magic_type = json.loads(self.description)['magic_type']
                    return magic_type
                except:
                    import traceback

                    traceback.print_exc()
        return 'unknown'


import libs.utils.transform as transform
import libs.utils.objTools as obj_tools


def get_ufs_obj_from_full_path(full_path):
    full_path = transform.transformDirToInternal(full_path)
    obj_list = UfsObj.objects.filter(full_path=full_path)
    if 0 == obj_list.count():
        ufs_url = obj_tools.getUfsUrlForPath(full_path)
        obj = UfsObj(ufs_url=ufs_url, full_path=full_path)
        obj.save()
    else:
        obj = obj_list[0]
    return obj


def get_ufs_obj_from_ufs_url(ufs_url):
    obj_list = UfsObj.objects.filter(ufs_url=ufs_url)
    if 0 == obj_list.count():
        obj = UfsObj(ufs_url=ufs_url)
        obj.save()
    else:
        obj = obj_list[0]
    return obj


try:
    import tagging

    tagging.register(UfsObj)
except:
    pass


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

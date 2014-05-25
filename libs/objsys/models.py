import uuid

from django.db import models
from django.contrib.auth.models import User


# Create your models here.


def get_new_uuid():
    return str(uuid.uuid4())


class Description(models.Model):
    content = models.TextField(null=True, blank=True, help_text="Content for the description")

    def __unicode__(self):
        return unicode(self.content)


class UfsObj(models.Model):
    full_path = models.TextField(null=True, blank=True)
    ufs_url = models.TextField(help_text='start with ufs:// or uuid:// etc.')
    uuid = models.CharField(max_length=60, default=get_new_uuid, unique=True,
                            help_text='the uuid string of the object, no "uuid" prefix needed')
    head_md5 = models.CharField(max_length=60, null=True, blank=True,
                                help_text="the md5 for the header of the object")
    total_md5 = models.CharField(max_length=60, null=True, blank=True,
                                 help_text="the entire object's md5 hash value")
    timestamp = models.DateTimeField('date this object record is published to database', auto_now_add=True)
    last_modified = models.DateTimeField('the last modified date for the object record in database', auto_now=True)

    obj_created = models.DateTimeField('the created date for the object itself', null=True, blank=True)
    obj_last_modified = models.DateTimeField('the last modified date for the object itself', null=True, blank=True)

    size = models.BigIntegerField(null=True, blank=True)
    user = models.ForeignKey(User, null=True, blank=True)
    description_json = models.TextField(null=True, blank=True, help_text="JSON description for this object")
    valid = models.BooleanField(default=True, help_text="is this field valid")
    relations = models.ManyToManyField("self", related_name='related_objs', null=True, blank=True,
                                       help_text="Related other information objects")
    descriptions = models.ManyToManyField(Description, related_name='descriptions', null=True, blank=True,
                                          help_text="Descriptions for this object")

    def __unicode__(self):
        return unicode(self.ufs_url + '---------> uuid:' + self.uuid)

    def save(self, *args, **kwargs):
        if not (self.full_path is None):
            try:
                from objsys_local.views import set_fields_from_full_path
                set_fields_from_full_path(self)
            except:
                pass
        super(UfsObj, self).save(*args, **kwargs)  # Call the "real" save() method.

    def get_type(self):
        if not (self.full_path is None):
            try:
                from objsys_local.views import get_type_from_full_path
                return get_type_from_full_path(self)
            except ImportError:
                pass
        return 'unknown'


class ObjRelation(models.Model):
    from_obj = models.ForeignKey(UfsObj, null=True, blank=True, related_name="from")
    to_obj = models.ForeignKey(UfsObj, null=True, blank=True, related_name="to")
    relation = models.CharField(max_length=60, null=True, blank=True,
                                help_text="relation text")
    valid = models.BooleanField(default=True, help_text="is this field valid")
    timestamp = models.DateTimeField('date this object is published to database', auto_now_add=True)
    last_modified = models.DateTimeField('the last modified date for the object in database', auto_now=True)


try:
    import tagging
    tagging.register(UfsObj)
except:
    pass

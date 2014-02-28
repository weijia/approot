from django.db.models.signals import post_save
from django.dispatch import receiver
from tagging.models import Tag, TaggedItem
from msg_service.auto_route_msg_service import AutoRouteMsgService
import time
from libs.obj_related.local_obj import LocalObj


def send_tagging_msg(instance):
    """
    self.put_item({"session_id": self.session_id, "ufs_url": obj.ufs_url, "uuid": obj.uuid, "full_path": obj.full_path,
                    "tag": obj_tag.name, "tag_app": obj_tag.tag_app, "timestamp": timestamp}, self.output)
    """
    b = AutoRouteMsgService().send_tagging_msg({"dynamic_tag": True,
                                                "ufs_url": instance.object.ufs_url,
                                                "uuid": instance.object.uuid,
                                                "full_path": instance.object.full_path,
                                                "timestamp": time.mktime(instance.timestamp.timetuple()),
                                                "tag": instance.tag.name,
                                                "tag_app": instance.tag_app})


@receiver(post_save, sender=TaggedItem)
def tagged_item_post_save(sender, instance, signal, *args, **kwargs):
    post = instance
    print "instance_tagged", instance.object.uuid, args, kwargs
    send_tagging_msg(instance)
from django.db.models.signals import post_save
from django.dispatch import receiver
from tagging.models import Tag, TaggedItem
from ui_framework.objsys.models import UfsObj
from libs.services.svc_base.beanstalkd_interface import beanstalkServiceBase
import beanstalkc
import time
from libs.obj_related.local_obj import LocalObj


@receiver(post_save, sender=TaggedItem)
def tagged_item_post_save(sender, instance, signal, *args, **kwargs):  
    post = instance
    print "instance_tagged", instance.object.uuid, args, kwargs
    '''
    #Moved to objsys/models.py
    modified = False
    try:
        local_obj = LocalObj(instance.object.full_path)
    
        if instance.object.size is None:
            instance.object.size = local_obj.get_size()
            modified = True
        if instance.object.description is None:
            instance.object.description = json.dumps({"magic_type": local_obj.get_type()})
            modified = True
        if modified:
            instance.object.save()
    except IOError:
        pass
    '''
    try:
        b = beanstalkServiceBase("all_tag_enumerator_service_global_input")
        '''
                self.put_item({"session_id": self.session_id, "ufs_url": obj.ufs_url, "uuid": obj.uuid, "full_path": obj.full_path, 
                        "tag": obj_tag.name, "tag_app": obj_tag.tag_app, "timestamp": timestamp}, self.output)

        '''
        b.addItem({"dynamic_tag": True,
                    "ufs_url": instance.object.ufs_url,
                    "uuid": instance.object.uuid,
                    "full_path": instance.object.full_path,
                    "timestamp": time.mktime(instance.timestamp.timetuple()),
                    "tag": instance.tag.name,
                    "tag_app": instance.tag_app})
                    
    except beanstalkc.SocketError:
        import traceback
        print 'can not connect to beanstalkd service'
        traceback.print_exc()
import uuid
from django.utils import timezone
from models import UfsObj
from models import CollectionItem
import django.db.utils
from django.contrib.auth.models import User, Group

from django.contrib import admin
from guardian.admin import GuardedModelAdmin
from ui_framework.normal_admin.admin import user_admin_site
from django.conf import settings
from guardian.shortcuts import assign


gRootUuid = u"4a5e8673-f2a2-4cf2-af6c-461fa9f31a15"

def register(objectClass, group_name = "scheduling"):
    module_name = objectClass.__module__.split(".")[0].lower()
    class_name = objectClass.__name__.lower()
    url = u"view://admin/%s/%s/add"%(module_name, class_name)
    try:
        for i in UfsObj.objects.filter(ufs_url = url):
            return
    except django.db.utils.DatabaseError:
        #Database is not created yet, just return, items will be created after syncdb is executed
        return
    o = UfsObj(ufs_url = url, uuid = unicode(uuid.uuid4()), timestamp=timezone.now(), user=User.objects.filter(username="AnonymousUser")[0])
    o.save()
    c = CollectionItem(obj = o, uuid = gRootUuid, id_in_col="%s_%s_add"%(module_name, class_name), 
                        timestamp=timezone.now(), user=User.objects.filter(username="AnonymousUser")[0])
    c.save()
    #Add to group
    try:
        group = Group.objects.filter(name=group_name)[0]
    except:
        #Group not exist, create it
        group = Group.objects.create(name=group_name)
    #print 'assigning: ', group, c
    assign('view_collection_item', group, c)

def get_item_id(parent_path):
    subitem_list = parent_path.split("/")
    parent_item_uuid = gRootUuid
    for i in subitem_list:
        #print 'getting uuid for item: ', i, ', parent:', parent_item_uuid, 'end'
        if i == "":
            continue
        parent_item_uuid = CollectionItem.objects.filter(uuid = parent_item_uuid, id_in_col = i)[0].obj.uuid
    #print 'returning parent', parent_item_uuid
    return parent_item_uuid
        
def register_menu(subitem_url, subitem_text, parent_path = "/", permmited_group = None):
    """
    If subitem_test contains dynamic, subitem_url is not used.
    Otherwise, subitem_url is the content of this menu item.
    Register a menu item in the left tree in object manager, the info is stored in objsys.models.Collection.
    :param subitem_url: menu item's URL. When the item is clicked, the URL will be loaded to the content pane
    :param subitem_text: menu item's text. It is stored in to id_in_col field for Collection and if it is
                            "dynamic://xxxx", the parent item's children will be dynamically generated by opening
                            URL: xxxx. xxxx should return a collection of items as in tags.tag_list. The format is
                            described in tags.tag_list as well.
    :param parent_path: the parent for this menu item. Root item is "/", sub menus should start with "/" as well.
    :param permmited_group:
    :return: N/A
    """
    root_uuid = get_item_id(parent_path)
    url = u"view://%s"%(subitem_url)
    qs = UfsObj.objects.filter(ufs_url = url)
    if True:#try:
        if 0 == qs.count():
            print 'creating new ufs obj'
            o = UfsObj(ufs_url = url, uuid = unicode(uuid.uuid4()), timestamp=timezone.now(), user=User.objects.filter(username="AnonymousUser")[0])
            o.save()
        else:
            #print 'use existing item'
            o = qs[0]
        
    else:#except django.db.utils.DatabaseError:
        #Database is not created yet, just return, items will be created after syncdb is executed
        return
    #print 'creating collection item for root: ', root_uuid
    if permmited_group is None:
        #If no permission requested, set anonymous user accessable.
        permitted_user_or_group = User.objects.filter(pk=settings.ANONYMOUS_USER_ID)[0]
    else:
        try:
            permitted_user_or_group = Group.objects.filter(name = permmited_group)[0]
        except:
            #Group not exist, create it
            permitted_user_or_group = Group.objects.create(name = permmited_group)
    collqs = CollectionItem.objects.filter(uuid = root_uuid, id_in_col = subitem_text)
    if 0 == collqs.count():
        c = CollectionItem(obj = o, uuid = root_uuid, id_in_col = subitem_text, 
                            timestamp=timezone.now(), user=User.objects.filter(username="AnonymousUser")[0])
        c.save()
    else:
        c = collqs[0]
    #Assign group permission

    assign('view_collection_item', permitted_user_or_group, c)

    

def register_to_sys(class_inst, admin_class = None):
    if admin_class is None:
        admin_class = type(class_inst.__name__+"Admin", (GuardedModelAdmin, ), {})
    try:
        admin.site.register(class_inst, admin_class)
    except:
        pass
    try:
        user_admin_site.register(class_inst, admin_class)
    except:
        pass
    #register(class_inst)


def register_all(class_list):
    for i in class_list:
        register_to_sys(i)
import libsys
from libs.services.svc_base.beanstalkd_interface import beanstalkWorkingThread
from libs.services.svc_base.gui_service import GuiService
import urllib
from django.conf import settings
from ui_framework.objsys.models import UfsObj
from tagging.models import Tag, TaggedItem
import tagging.models
import os
from libs.utils.transform import transformDirToInternal
from django.contrib.auth.models import User
import libs.utils.filetools as filetools
import libs.utils.objTools as objtools

gDefaultServices = ['monitor',
                'scache_storage',
                'tagged_enumerator',
                'tube_logging_service',
                'git_puller',
                're_send_service',
                'tag_exporter',
                'tag_importer',
                'delay_send_service',
                'domain_assign_service',
                #'folder_tagging',
                'all_tag_enumerator',
                'tube_folder_tagging',
                'diagram_importer',
                ]
        
def init_all_tagged_apps():
    '''
    * Create initial processor items from /libs/services/apps/
    * Operations for each script if not exists in db: UfsObj(ufs_url="file:///script-path.py").tag=system:app
    * object tagged with system:app will be a processor.
    * Then all processors will be started as server.
    '''
    #print 'POSTGRESQL_PORT:', os.environ.get("POSTGRESQL_PORT")
    tag = u'system:auto-app'
    #root_dir = libsys.get_root_dir()
    #app_folder = os.path.join(root_dir, "libs/services/apps/")
    for appname in gDefaultServices:
        #print app
        app = filetools.findAppInProduct(appname)
        if app is None:
            print 'app: ', appname, 'does not exist'
            continue
        name, ext = os.path.splitext(app)
        #print ext
        if ext in ['.py', '.exe']:
            full_path = transformDirToInternal(app)
            #url = u"file:///" + full_path
            #print url
            #Tag object
            try:
                objs = UfsObj.objects.filter(full_path = full_path)
                if 0 != len(objs):
                    for obj in objs:
                        obj.tags = tag
                else:
                    raise UfsObj.DoesNotExist
            except UfsObj.DoesNotExist:
                #print "Create new item"
                import uuid
                from django.utils import timezone
                user = User.objects.all()[0]
                #obj = UfsObj(ufs_url = url, uuid = unicode(uuid.uuid4()), timestamp=timezone.now(), user = user)
                ufs_url = objtools.getUfsUrlForPath(full_path)
                obj = UfsObj(ufs_url = ufs_url, uuid = unicode(uuid.uuid4()), timestamp=timezone.now(), user = user, full_path = full_path)

                obj.save()
                obj.tags = tag

    try:
        obj_tag = Tag.objects.get(name=tag)
        objs = TaggedItem.objects.get_by_model(UfsObj, obj_tag)
    except:
        return

    res = []
    for obj in objs:
        path = obj.full_path
        #Use only the filename? so we need to avoid apps with the same name?
        if not os.path.exists(path):
            base = os.path.basename(path).split(".")[0]
            path = filetools.findAppInProduct(base)
            if not os.path.exists(path):
                obj.delete()
                return
        gui_service = GuiService()
        gui_service.addItem({"command": "Launch", "path": path, "param":['--startserver']})
        #The following is used to test duplicated service launching
        #if 'tube_logging' in path:
        #    gui_service.addItem({"command": "Launch", "path": path, "param":['--startserver']})

        
if __name__ == "__main__":
    init_all_tagged_apps()
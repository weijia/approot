import os
from libtool import find_root_path
from libtool.filetools import collect_files_in_dir, find_callable_in_app_framework
from objsys.view_utils import get_ufs_obj_from_full_path
from utils.django_utils import get_content_item_list_in_tastypie_format


class App(object):
    """
    Can not be called directly
    """
    def get_info(self):
        ufs_obj = get_ufs_obj_from_full_path(self.app_full_path)
        return {"data": self.app_name, "full_path": ufs_obj.full_path, "ufs_url": ufs_obj.ufs_url,
                "description": ufs_obj.ufs_url}


class FullPathApp(App):
    def __init__(self, app_full_path):
        self.app_full_path = app_full_path
        self.app_name = os.path.basename(self.app_full_path).split(".")[0]


class NamedApp(App):
    def __init__(self, app_name):
        self.app_name = app_name
        self.app_full_path = app_path = find_callable_in_app_framework(self.app_name)
        if app_path is None:
            raise "Obj not exists"


gIgnoreAppList = ["root.exe", "__init__.py", "libsys.py",
                  "postgresql.bat",
                  "postgresql_stop.bat",
                  "start_ext.bat",
                  "start_ext_app.bat",
                  "startBeanstalkd.bat",
                  #"mongodb.bat"
                  #"syncdb.bat",
                  #"tornado.bat",
                  #"tornado_app.bat",
                  #"runserver.bat",
                  #"makedoc.bat"
                  #"activate.bat"
                  #"activate_app.bat",
                  #"cmd_prompt.bat"
]


def list_in_tastypie_format(request):
    app_list = get_service_app_list()
    return get_content_item_list_in_tastypie_format(app_list)


def get_service_app_list():
    app_path_list = []
    #for app_name in gDefaultServices:
    #    app_list.append(NamedApp(app_name))
    #Add root folder .exe, (used for built apps)
    root_dir = find_root_path(__file__, "approot")
    for sub_dir, ext in [("/", ".exe"), ("libs/services/simple_app/", ".py"),
                         ("libs/services/external_app/", ".bat"),
                         ("/external/", ".bat")]:
        sub_dir_full_path = os.path.join(root_dir, sub_dir)
        app_path_list.extend(collect_files_in_dir(sub_dir_full_path, ext, gIgnoreAppList))
    app_list = []
    for full_path in app_path_list:
        app_list.append(FullPathApp(full_path))
    return app_list
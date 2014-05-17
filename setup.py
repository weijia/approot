#from setuptools import find_packages
import os
import pprint
import sys
from libtool import include_sub_folder_in_root_path
include_sub_folder_in_root_path(__file__, "approot", "libs")

from cx_Freeze import setup, Executable
from django_build.django_setup import DjangoCxFreezeBuildSpecGenerator
from extra_settings.init_settings import init_settings
from libtool import filetools


def gen_executable_list(script_list):
    executable_list = []
    for i in script_list:
        app = create_executable_from_app_name(i)
        if app is None:
            continue
        executable_list.append(app)
    return executable_list


def create_executable_from_app_name(app_param):
    if type(app_param) != tuple:
        app_full_name = app_param + ".py"
        app_path = filetools.find_filename_in_app_framework_with_pattern(app_full_name)
        if app_path is None:
            return None
            #print "app:", app_path
        return Executable(script=app_path)
    else:
        app_full_name = app_param[0] + ".py"
        app_path = filetools.find_filename_in_app_framework_with_pattern(app_full_name)
        #print "app with target:", app_path
        return Executable(script=app_path, targetName=app_param[1])


###########################
# Add python module that is not automatically included in the build below. Such as Django app
# file with special names other than: models, urls, admin, views etc.
###########################
includes = [
    #os.environ["DJANGO_SETTINGS_MODULE"], #rootapp
    "PyQt4.QtCore",
    "pkg_resources",#Used by pytz to load time zone info in zoneinfo folder
    "yaml",
    "rootapp.urls",
    "rootapp.settings",
    "extra_settings.settings",
    "extra_settings.build_settings",
    "djangoautoconf",
    "djangoautoconf.sqlite_database",
    "djangoautoconf.features.guardian",
    "djangoautoconf.features.pagination",
    "djangoautoconf.features.django_social_auth",
    "djangoautoconf.features.django_registration",
    "connection.save_diagram_view",
    #"tags.tag_utils",
    #"objsys.tree",
    #"manifest",
    "ui_framework",
    'django',
    'magic',
    'desktop.filemanager.folder_view',
    #'libs.custom_collections',
    'custom_collections.modules.local_filesystem',
    'obj_operation.service_op',
    'ui_framework.manifest',
    #For Cherrypy
    #"django.contrib.messages",
    "email",
    "email.message",
    "cherrypy",
    "iconizer",
    "libtool",
    "keys",
    #For social auth
    "social_auth.db.django_models",
    #For registration
    'registration.backends.default.urls',
    'registration.auth_urls',
    #'rootapp.separated_settings.build_settings',
    #'rootapp.separated_settings.local_postgresql_settings',
    "django.core.management",
    "django.core.management.commands.syncdb",
    "django.core.management.commands.loaddata",
    'south.management.commands.syncdb',
    'south.management.commands.migrate',
]

app_list = ['new_rootapp',
            #'tornado_main',
            'tagging',
            'new_ext_svr',
            "name_server_app",
            #'sftpserver',
            #'BeanstalkdLauncherService',
            #'manage',
            #'syncdb'
            #'initial_launcher',
            'cherrypy_server',
            #'service_starter',
            #'msg_based_service_mgr',
            # ('monitor.py', 'libs/services/apps/monitor.exe'),
            # ('scache_storage.py', 'libs/services/apps/scache_storage.exe'),
            # ('tagged_enumerator.py', 'libs/services/apps/tagged_enumerator.exe'),
            # ('tube_logging.py', 'libs/services/apps/tube_logging.exe'),
]
from services.svc_base.default_apps import gDefaultServices

app_list.extend(gDefaultServices)
print app_list, '-------------------'
from iconizer.qtconsole.fileTools import find_resource_in_pkg

include_files = []


def get_iconizer_resources():
    result = []
    for i in ["gf-16x16.png", "list_window.ui", "droppable.ui", "notification.ui"]:
        result.append((find_resource_in_pkg(i), i))
    return result


include_files.extend(get_iconizer_resources())
include_files.extend([
    #("libs/services/external_app/startBeanstalkd.bat", "startBeanstalkd.bat"),
    #("libs/services/external_app/scache.bat", "external_app/scache.bat"),
    #("libs/services/external_app/sftpserver.bat", "external_app/sftpserver.bat"),
    ("libs/services/external_app/postgresql.bat", "postgresql.bat"),
    ("libs/services/external_app/postgresql_stop.bat", "postgresql_stop.bat"),
    #("libs/services/external_app/start_ext_app.bat", "start_ext.bat"),
    #("libs/services/apps/diagrams/", "diagrams"),
    #("libs/allauth/fixtures/initial_data.json", "initial_data.json"),
    ("libs/zlib1.dll", "libs/zlib1.dll"),
    ("libs/regex2.dll", "libs/regex2.dll"),
    ("libs/magic1.dll", "libs/magic1.dll"),
    #("tornado_app.bat", "tornado.bat"),
    #("activate_app.bat", "activate.bat"),
    #("syncdb.bat", "syncdb.bat"),
    ("share", "share"),
    ("keys", "keys"),
    #("../others", "../others"),
])

excludefiles = []


def get_pytz_files():
    path_base = "D:\\work\\mine\\venv\\Lib\\site-packages\\pytz\\zoneinfo\\"
    exe_path = os.path.dirname(sys.executable)
    if "Scripts" in exe_path:
        exe_path = os.path.dirname(exe_path)
    path_base = os.path.join(exe_path, "Lib\\site-packages\\pytz\\zoneinfo\\")
    skip_count = len(path_base)
    zip_includes = [(path_base, "pytz/zoneinfo/")]
    for root, sub_folders, files in os.walk(path_base):
        for file_in_root in files:
            zip_includes.append(
                ("{}".format(os.path.join(root, file_in_root)),
                 "{}".format(os.path.join("pytz/zoneinfo", root[skip_count:], file_in_root))
                )
            )
    return zip_includes


zip_includes = get_pytz_files()
build_exe_dir = "../build/approot"

build_exe_params = {
    "includes": includes,
    'include_files': include_files,
    "bin_excludes": excludefiles,
    "build_exe": build_exe_dir,
    "zip_includes": zip_includes,
    #"packages": find_packages(),
}


#Create data.db for SQLITE so build process can run with SQLITE
os.environ["POSTGRESQL_ROOT"] = ""
settings_module = init_settings().get_settings()
os.system("syncdb.bat")
os.system(sys.executable + " ./manage.py migrate")
os.system("collectstatic.bat")
os.system("collectcmd.bat")

#Need to remove port_v3 for QT for cx_freeze when packaging PyQt


#Workarround for cx_freeze packaging cherrypy
import _tkinter
from os.path import dirname

python_dir = dirname(dirname(_tkinter.__file__))
tcl_lib_path_name = "tcl/tcl" + _tkinter.TCL_VERSION
tk_lib_path_name = "tcl/tk" + _tkinter.TCL_VERSION
os.environ["TCL_LIBRARY"] = os.path.join(python_dir, tcl_lib_path_name)
os.environ["TK_LIBRARY"] = os.path.join(python_dir, tk_lib_path_name)

print os.environ["DJANGO_SETTINGS_MODULE"], '---------------------------'
#print dir(rootapp.ufs_django_settings.get_settings())

DjangoCxFreezeBuildSpecGenerator().gen_spec(settings_module, build_exe_params)

final_script_list = gen_executable_list(app_list)
pprint.pprint(build_exe_params)
setup(
    version="0.1", #This is required or build process will have exception.
    description="application starter",
    options={"build_exe": build_exe_params},
    executables=final_script_list,
    #include_package_data=True,
    #package_data = {'':['*.*', 'templates/*.*']},
    #packages = find_packages(),
)

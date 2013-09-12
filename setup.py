#from setuptools import find_packages
import os

from cx_Freeze import setup, Executable

#from rootapp import settings
from libs.django_build.django_setup import DjangoCxFreezeBuildSpecGenerator
import libs.utils.filetools as filetools
import rootapp.ufs_django_settings

####################
# Dependancy
####################
# pspcopg: http://www.stickpeople.com/projects/python/win-psycopg/2.5.0/psycopg2-2.5.win32-py2.7-pg9.2.4-release.exe
# pyyaml: pip install pyyaml
# pyopenssl: https://pypi.python.org/pypi/pyOpenSSL
# pip install django-tastypie
# pip install pyyaml
#


def gen_executables_list(script_list):
    executable_list = []
    for i in script_list:
        app = get_executable(i)
        if app is None:
            continue
        executable_list.append(app)
    return executable_list


def get_executable(app_param):
    if type(app_param) != tuple:
        app_full_name = app_param + ".py"
        app_path = filetools.findFileInProduct(app_full_name)
        if app_path is None:
            return None
            #print "app:", app_path
        return Executable(script=app_path)
    else:
        app_full_name = app_param[0] + ".py"
        app_path = filetools.findFileInProduct(app_full_name)
        #print "app with target:", app_path
        return Executable(script=app_path, targetName=app_param[1])


###########################
# Add python module that is not automatically included in the build below. Such as Django app
# file with special names other than: models, urls, admin, views etc.
###########################
includes = [
    #os.environ["DJANGO_SETTINGS_MODULE"], #rootapp
    "PyQt4.QtCore",
    "yaml",
    "rootapp.urls",
    "ui_framework.connection.save_diagram_view",
    "ui_framework.manifest",
    'django',
    'magic',
    'desktop.filemanager.folder_view',
    #'libs.custom_collections',
    'libs.custom_collections.modules.local_filesystem',
    #For Cherrypy
    #"django.contrib.messages",
    "email",
    "email.message",
    "cherrypy",
    #For social auth
    "social_auth.db.django_models",
    #For registration
    'registration.backends.default.urls',
    'registration.auth_urls'
]

script_list = ['new_rootapp',
               #'tornado_main',
               'tagging', 'new_ext_svr', 'sftpserver',
               #'BeanstalkdLauncherService',
               #'manage',
               #'syncdb'
               #'initial_launcher',
               'cherrypy_server',
               'service_starter', 'msg_based_service_mgr',
               # ('monitor.py', 'libs/services/apps/monitor.exe'),
               # ('scache_storage.py', 'libs/services/apps/scache_storage.exe'),
               # ('tagged_enumerator.py', 'libs/services/apps/tagged_enumerator.exe'),
               # ('tube_logging.py', 'libs/services/apps/tube_logging.exe'),
]
from libs.services.svc_base.default_apps import gDefaultServices

script_list.extend(gDefaultServices)
print script_list, '-------------------'
from iconizer.qtconsole.fileTools import find_resource_in_pkg

includefiles = [
    (find_resource_in_pkg("gf-16x16.png"), "gf-16x16.png"),
    (find_resource_in_pkg("app_list.ui"), "app_list.ui"),
    (find_resource_in_pkg("droppable.ui"), "droppable.ui"),
    (find_resource_in_pkg("notification.ui"), "notification.ui"),
    ("libs/services/external_app/startBeanstalkd.bat", "startBeanstalkd.bat"),
    ("libs/services/external_app/scache.bat", "external_app/scache.bat"),
    ("libs/services/external_app/sftpserver.bat", "external_app/sftpserver.bat"),
    ("libs/services/external_app/postgresql.bat", "postgresql.bat"),
    ("libs/services/external_app/postgresql_stop.bat", "postgresql_stop.bat"),
    ("libs/services/external_app/start_ext_app.bat", "start_ext.bat"),
    ("libs/services/apps/diagrams/", "diagrams"),
    #("libs/allauth/fixtures/initial_data.json", "initial_data.json"),
    ("libs/zlib1.dll", "libs/zlib1.dll"),
    ("libs/regex2.dll", "libs/regex2.dll"),
    ("libs/magic1.dll", "libs/magic1.dll"),
    #("tornado_app.bat", "tornado.bat"),
    ("activate_app.bat", "activate.bat"),
    #("syncdb.bat", "syncdb.bat"),
    ("share", "share"),
    #("../others", "../others"),
]
excludefiles = []
zip_includes = []
build_exe_dir = "../build/approot"

build_exe_params = {
    "includes": includes,
    'include_files': includefiles,
    "bin_excludes": excludefiles,
    "build_exe": build_exe_dir,
    "zip_includes": zip_includes,
    #"packages": find_packages(),
}


#Create data.db for SQLITE so build process can run with SQLITE
os.environ["POSTGRESQL_ROOT"] = ""
os.system("syncdb.bat")
os.system("collectstatic.bat")

#Need to remove port_v3 for QT for cx_freeze when packaging PyQt


#Workarround for cx_freeze packaging cherrypy
import _tkinter
from os.path import dirname

python_dir = dirname(dirname(_tkinter.__file__))

#print os.environ["TCL_LIBRARY"]
#print os.environ["TK_LIBRARY"]
#os.environ["TCL_LIBRARY"] = os.path.join(python_dir, "tcl/tcl8.5")
#os.environ["TK_LIBRARY"] = os.path.join(python_dir, "tcl/tk8.5")

tcl_lib_path_name = "tcl/tcl" + _tkinter.TCL_VERSION
tk_lib_path_name = "tcl/tk" + _tkinter.TCL_VERSION

os.environ["TCL_LIBRARY"] = os.path.join(python_dir, tcl_lib_path_name)
os.environ["TK_LIBRARY"] = os.path.join(python_dir, tk_lib_path_name)

print os.environ["DJANGO_SETTINGS_MODULE"], '---------------------------'
'''
settings_package = __import__(os.environ["DJANGO_SETTINGS_MODULE"])
print dir(settings_package)
print os.environ["DJANGO_SETTINGS_MODULE"].rsplit('.', 1)[1]
settings_module = getattr(settings_package, os.environ["DJANGO_SETTINGS_MODULE"].rsplit('.', 1)[1])
'''
print dir(rootapp.ufs_django_settings.get_settings())
settings_module = rootapp.ufs_django_settings.get_settings()
DjangoCxFreezeBuildSpecGenerator().gen_spec(settings_module, build_exe_params)

final_script_list = gen_executables_list(script_list)
print build_exe_params
setup(
    version="0.1", #This is required or build process will have exception.
    description="application starter",
    options={"build_exe": build_exe_params},
    executables=final_script_list,
    #include_package_data=True,
    #package_data = {'':['*.*', 'templates/*.*']},
    #packages = find_packages(),
)
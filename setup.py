import libsys
#from setuptools import find_packages
from rootapp import settings
from cx_Freeze import setup, Executable
from django_setup import gen_spec
import os
import libs.qtconsole.fileTools as filetools

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


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "rootapp.settings")

###########################
# Add python module that is not automatically included in the build below. Such as Django app
# file with special names other than: models, urls, admin, views etc.
###########################
includes = ["PyQt4.QtCore",
            "yaml",
            "rootapp.settings",
            "rootapp.urls",
            "ui_framework.connection.save_diagram_view",
            "ui_framework.manifest",
            'django',
            'magic',
            'desktop.filemanager.folder_view',
            #'libs.custom_collections',
            'libs.custom_collections.modules.local_filesystem'
]

script_list = ['rootapp', 'tornado_main', 'tagging', 'ext_svr', 'sftpserver',
               'BeanstalkdLauncherService', 'manage', 'initial_launcher',
               'service_starter',
               # ('monitor.py', 'libs/services/apps/monitor.exe'),
               # ('scache_storage.py', 'libs/services/apps/scache_storage.exe'),
               # ('tagged_enumerator.py', 'libs/services/apps/tagged_enumerator.exe'),
               # ('tube_logging.py', 'libs/services/apps/tube_logging.exe'),
]
from libs.services.initial_launcher import gDefaultServices

script_list.extend(gDefaultServices)
print script_list

includefiles = [("libs/qtconsole/gf-16x16.png", "gf-16x16.png"),
                ("libs/qtconsole/app_list.ui", "app_list.ui"),
                ("libs/qtconsole/droppable.ui", "droppable.ui"),
                ("libs/qtconsole/notification.ui", "notification.ui"),
                ("libs/services/external_app/startBeanstalkd.bat", "startBeanstalkd.bat"),
                ("libs/services/external_app/scache.bat", "scache.bat"),
                ("libs/services/external_app/sftpserver.bat", "sftpserver.bat"),
                ("libs/services/external_app/postgresql.bat", "postgresql.bat"),
                ("libs/services/external_app/postgresql_stop.bat", "postgresql_stop.bat"),
                ("libs/services/external_app/start_ext_app.bat", "start_ext.bat"),
                ("libs/allauth/fixtures/initial_data.json", "initial_data.json"),
                ("libs/zlib1.dll", "libs/zlib1.dll"),
                ("libs/regex2.dll", "libs/regex2.dll"),
                ("libs/magic1.dll", "libs/magic1.dll"),
                ("tornado_app.bat", "tornado.bat"),
                ("activate_app.bat", "activate.bat"),
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

gen_spec(settings, build_exe_params)

final_script_list = gen_executables_list(script_list)

setup(
    version="0.1", #This is required or build process will have exception.
    description="application starter",
    options={"build_exe": build_exe_params},
    executables=final_script_list,
    #include_package_data=True,
    #package_data = {'':['*.*', 'templates/*.*']},
    #packages = find_packages(),
)
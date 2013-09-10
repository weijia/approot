import pprint
import libs.root_lib_sys
#import libs.qtconsole.fileTools as file_tools
import os


def add_django_module(class_list, includes):
    for i in class_list:
        module_name = i.split(".")[0:-1]
        if not (module_name in includes):
            includes.append(".".join(module_name))


def add_django_module_from_list(module_list, includes):
    for i in module_list:
        add_django_module(i, includes)

def get_other_processor_modules(settings):
    res = []
    for i in ['MIDDLEWARE_CLASSES', 'AUTHENTICATION_BACKENDS',
                                 'TEMPLATE_CONTEXT_PROCESSORS', 'TEMPLATE_LOADERS']:
        try:
            res += getattr(settings, i)
        except AttributeError:
            print "no attr:", i
    return res
        

def gen_spec(settings, existing_config):
    print dir(settings)
    for loaded_django_app in settings.INSTALLED_APPS:
        #print i
        try:
            module_i = __import__(loaded_django_app)
        except ImportError, e:
            import sys
            print "no app:", loaded_django_app

            pprint.pprint(sys.path)
            raise

        #print 'name:', module_i.__name__
        #print 'full name:', i
        #print i.split(".")[1:]
        module_path = "/".join(loaded_django_app.split(".")[1:])
        #print module_path
        module_root = os.path.join(module_i.__path__[0], module_path)
        #print module_i.__path__

        possible_template_path = os.path.join(module_root, 'templatetags')

        #print 'template tag path:',possible_template_path
        if os.path.exists(possible_template_path):
            for templatetags_file in os.listdir(possible_template_path):
                name, ext = os.path.splitext(templatetags_file)
                if ext == ".py":
                    #print 'templatetags file:',templatetags_file
                    templatetags_file_full_path = os.path.join(possible_template_path, templatetags_file)

                    if not os.path.isdir(templatetags_file_full_path):
                        existing_config['includes'].append(loaded_django_app + ".templatetags." + name)
                        #print i+".templatetags."+name




        #################################################3
        #Install template/static files to target dir
        ##############################################
        for django_data_folder in ['templates']:
            #print module_root
            data_folder = os.path.join(module_root, django_data_folder)
            #print data_folder
            if os.path.exists(data_folder):
                #folders.append(data_folder)
                #existing_config['include_files'].append((data_folder, 
                #                        os.path.join(i.replace('.', '/'), django_data_folder)))
                #                        
                #existing_config['zip_includes'].append((data_folder, 
                #                        os.path.join(i.replace('.', '/'), django_data_folder)))
                existing_config['include_files'].append((data_folder,
                                                         'templates'))

        for django_sub_module in ['urls', 'views', 'admin', 'api', 'models', 'forms', 'decorators', 'mixins',
                                  'management']:
            try:
                print loaded_django_app + "." + django_sub_module
                sub_module = __import__(loaded_django_app + "." + django_sub_module)
                existing_config['includes'].append(loaded_django_app + "." + django_sub_module)
            except ImportError, e:
                #print e
                #print e.message
                #print e.args
                if ("No module named %s" % django_sub_module) == e.message:
                    continue
                #raise

                #########
                # TODO: import module from url
                #########
    existing_config['includes'].extend([
        #"psycopg2",
        "django.core.cache.backends.locmem",
        "django.core.serializers.xml_serializer",
        "django.core.serializers.python",
        "django.core.serializers.json",
        "django.core.serializers.pyyaml",
        'django.template.defaulttags',
        'django.template.defaultfilters',
        'django.template.loader_tags',
        'django.template.loaders.filesystem',
        'django.template.loaders.app_directories',
        'django.contrib.sessions.backends.db',
        'django.contrib.auth.models',
        'django.contrib.messages.storage.fallback',
        'django.contrib.sites',
        'django.contrib.sites.managers',
        'django.contrib.sites.management',
        'django.contrib.admin',
        'django.contrib.admin.models',
        'django.contrib.admin.sites',
        'django.contrib.admin.forms',
        "django.contrib.sessions",


        'django.db.models',
        'django.db.backends.sqlite3',
        "django.db.models.sql.compiler",
        "django.db.backends.postgresql_psycopg2",
        "django.db.backends.postgresql_psycopg2.base",

        'django.templatetags.i18n',
        'django.templatetags.l10n',
        'django.templatetags.static',
        'django.templatetags.cache',
        'django.templatetags.tz',
        'django.templatetags.future',
        'django.views.i18n',
        'django.views.csrf',
        'django.views.defaults',
        'django.views.static',
        'django.views.debug',
        'django.views.generic.simple',
        'django.conf.urls.defaults',
        'django.dispatch.dispatcher',

        #Needed when using cherrypy, copied from http://blog.robotercoding.com/?p=124
        'email.mime.audio',
        'email.mime.base',
        'email.mime.image',
        'email.mime.message',
        'email.mime.multipart',
        'email.mime.nonmultipart',
        'email.mime.text',
        'email.charset',
        'email.encoders',
        'email.errors',
        'email.feedparser',
        'email.generator',
        'email.header',
        'email.iterators',
        'email.message',
        'email.parser',
        'email.utils',
        'email.base64mime',
        'email.quoprimime',


        #"django.middleware.common",
        #"django.contrib.sessions.middleware",
        "management",
        "management.commands.syncdb",
        "management.commands.loaddata",
        ##############
        #"allauth",
        #"allauth.account",
        "argparse",
        #"allauth.socialaccount",
        "guardian",
        "win_smb",
        "ui_framework",
        "ui_framework.collection_management",
        "ui_framework.normal_admin",
        "ui_framework.objsys",
        "tags",
        "ui_framework.connection",
        "desktop.filemanager",
        #"thumbapp.views"
    ]
    )

    add_django_module_from_list(get_other_processor_modules(settings),
                                existing_config['includes'])
    existing_config['includes'].extend(settings.INSTALLED_APPS)

    existing_config['include_files'].append("static")
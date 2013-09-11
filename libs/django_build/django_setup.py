import pprint
import libs.root_lib_sys
#import libs.qtconsole.fileTools as file_tools
import os
from default_module_list import DEFAULT_DJANGO_MODULES


def add_django_module(class_list, includes):
    for i in class_list:
        module_name = i.split(".")[0:-1]
        if not (module_name in includes):
            includes.append(".".join(module_name))


def add_django_module_from_list(module_list, includes):
    for i in module_list:
        #print i, '[[[[[[[[[[[[[[[[[[[[['
        add_django_module(i, includes)


def get_other_processor_modules(settings):
    res = []
    for i in ['MIDDLEWARE_CLASSES', 'AUTHENTICATION_BACKENDS',
              'TEMPLATE_CONTEXT_PROCESSORS', 'TEMPLATE_LOADERS']:
        try:
            #print getattr(settings, i), '----------------------'
            res.append(getattr(settings, i))
        except AttributeError:
            print "no attr:", i
        #print res, '============================'
    return res


def include_default_files_in_django_app(existing_config, loaded_django_app):
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
                pass
                #raise

                #########
                # TODO: import module from url
                #########


def include_data_for_django_app(existing_config, module_root):
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


def include_templatetags_in_django_app(existing_config, loaded_django_app, module_root):
    possible_templatetags_folder = os.path.join(module_root, 'templatetags')
    #print 'template tag path:',possible_template_path
    if os.path.exists(possible_templatetags_folder):
        for templatetags_file in os.listdir(possible_templatetags_folder):
            name, ext = os.path.splitext(templatetags_file)
            if ext == ".py":
                #print 'templatetags file:',templatetags_file
                templatetags_file_full_path = os.path.join(possible_templatetags_folder, templatetags_file)

                if not os.path.isdir(templatetags_file_full_path):
                    existing_config['includes'].append(loaded_django_app + ".templatetags." + name)
                    #print i+".templatetags."+name


def update_config_spec_for_installed_apps(existing_config, loaded_django_app):
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
    include_templatetags_in_django_app(existing_config, loaded_django_app, module_root)
    include_data_for_django_app(existing_config, module_root)
    include_default_files_in_django_app(existing_config, loaded_django_app)




class DjangoCxFreezeBuildSpecGenerator(object):
    def gen_spec(self, settings, existing_config):
        print dir(settings)
        for loaded_django_app in settings.INSTALLED_APPS:
            update_config_spec_for_installed_apps(existing_config, loaded_django_app)

        existing_config['includes'].extend(DEFAULT_DJANGO_MODULES
        )
        #print existing_config['includes']
        add_django_module_from_list(get_other_processor_modules(settings),
                                    existing_config['includes'])
        #print existing_config['includes'], '!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!1'

        existing_config['includes'].extend(settings.INSTALLED_APPS)

        existing_config['include_files'].append("static")
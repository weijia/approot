import pprint
import libs.root_lib_sys
#import libs.qtconsole.fileTools as file_tools
import os
from default_module_list import DEFAULT_DJANGO_MODULES


class DjangoCxFreezeBuildSpecGenerator(object):
    def __init__(self):
        self.existing_config = None

    def add_module_to_includes(self, item):
        if type(item) == list:
            raise "No list permitted"
        if not (item in self.existing_config['includes']):
            self.existing_config['includes'].append(item)

    def extend_includes(self, includes_list):
        for item in includes_list:
            self.add_module_to_includes(item)

    def get_module_name_from_class_name(self, class_name):
        return ".".join(class_name.split(".")[0:-1])

    def add_modules_from_class_name_list(self, class_name_list):
        for clss_name_for_import in class_name_list:
            #print i, '[[[[[[[[[[[[[[[[[[[[['
            self.add_module_to_includes(self.get_module_name_from_class_name(clss_name_for_import))

    def gen_spec(self, settings, existing_config):
        self.existing_config = existing_config
        print dir(settings)
        for installed_app in settings.INSTALLED_APPS:
            self.update_config_spec_for_django_app(installed_app)

        self.extend_includes(DEFAULT_DJANGO_MODULES)
        #print existing_config['includes']
        self.add_modules_from_class_name_list(self.get_class_names_included_in_settings(settings))
        #print existing_config['includes'], '!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!1'

        self.extend_includes(settings.INSTALLED_APPS)
        self.existing_config['include_files'].append("static")

    def get_class_names_included_in_settings(self, settings):
        res = []
        for i in ['MIDDLEWARE_CLASSES', 'AUTHENTICATION_BACKENDS',
                  'TEMPLATE_CONTEXT_PROCESSORS', 'TEMPLATE_LOADERS']:
            try:
                #print getattr(settings, i), '----------------------'
                res.extend(getattr(settings, i))
            except AttributeError:
                print "no attr:", i
                #print res, '============================'
        return res

    def add_templatetags_modules(self, django_app_name, module_root):
        possible_templatetags_folder = os.path.join(module_root, 'templatetags')
        #print 'template tag path:',possible_template_path
        if os.path.exists(possible_templatetags_folder):
            for templatetags_file in os.listdir(possible_templatetags_folder):
                name, ext = os.path.splitext(templatetags_file)
                if ext == ".py":
                    #print 'templatetags file:',templatetags_file
                    templatetags_file_full_path = os.path.join(possible_templatetags_folder, templatetags_file)

                    if not os.path.isdir(templatetags_file_full_path):
                        self.add_module_to_includes(django_app_name + ".templatetags." + name)
                        #print i+".templatetags."+name

    def include_default_files_in_django_app(self, django_app_name):
        for django_sub_module in ['urls', 'views', 'admin', 'api', 'models', 'forms', 'decorators', 'mixins',
                                  'management']:
            try:
                #print django_app_name + "." + django_sub_module
                sub_module = __import__(django_app_name + "." + django_sub_module)
                self.add_module_to_includes(django_app_name + "." + django_sub_module)
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

    def add_templates(self, module_root):
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
                self.existing_config['include_files'].append((data_folder,
                                                              'templates'))

    def update_config_spec_for_django_app(self, django_app_name):
        #print i
        try:
            module_i = __import__(django_app_name)
        except ImportError, e:
            print "no app:", django_app_name
            import sys

            pprint.pprint(sys.path)
            raise

        #print 'name:', module_i.__name__
        #print 'full name:', i
        #print i.split(".")[1:]
        module_path = "/".join(django_app_name.split(".")[1:])
        #print module_path
        module_root = os.path.join(module_i.__path__[0], module_path)
        #print module_i.__path__
        self.add_templatetags_modules(django_app_name, module_root)
        self.add_templates(module_root)
        self.include_default_files_in_django_app(django_app_name)
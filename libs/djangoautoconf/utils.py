import importlib
import logging


log = logging.getLogger(__name__)


def inject_attributes(target_class, src_module, exclude=[]):
    target_instance = target_class()
    for attr in dir(src_module):
        if attr != attr.upper():
            continue
        if attr in exclude:
            continue
        value = getattr(src_module, attr)
        setattr(target_instance.__class__, attr, value)
        #print "setting attr:", attr, value


def dump_attrs(obj_instance):
    for attr in dir(obj_instance):
        if attr != attr.upper():
            continue
        log.debug(attr+" : "+str(getattr(obj_instance, attr)))


def get_class(django_cb_class_full_name):
    settings_module = importlib.import_module(get_module_name_from_str(django_cb_class_full_name))
    #print settings_module
    #print getattr(settings_module, get_class_name_from_str(settings_class_str))
    return getattr(settings_module, get_class_name_from_str(django_cb_class_full_name))().__class__
    #return getattr(settings_module, get_settings_class_name()).__class__


def get_module_name_from_str(importing_class_name):
    #print importing_class_name.rsplit('.', 1)[0]
    return importing_class_name.rsplit('.', 1)[0]


def get_class_name_from_str(importing_class_name):
    #print importing_class_name.rsplit('.', 1)[1]
    return importing_class_name.rsplit('.', 1)[1]


def validate_required_attributes(setting_class_instance):
    if setting_class_instance.DATABASES["default"]["ENGINE"] == 'django.db.backends.dummy':
        raise "Invalid database"
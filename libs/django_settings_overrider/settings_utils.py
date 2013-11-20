from rootapp import customized_settings

__author__ = 'q19420'


def inject_attributes(target_class, src_module):
    target_instance = target_class()
    for attr in dir(src_module):
        if attr != attr.upper():
            continue
        setattr(target_instance.__class__, attr, getattr(customized_settings, attr))
import os
#os.environ.setdefault("DJANGO_SETTINGS_MODULE", "rootapp.customized_settings")
os.environ.setdefault('DJANGO_SETTINGS_FACTORY', 'rootapp.cbsettings_root.RootSettings')
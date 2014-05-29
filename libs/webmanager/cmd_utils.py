try:
    from django_commands_dict import django_commands_dict
except ImportError:
    django_commands_dict = None


import django.core.management as core_management


from default_user_conf import *


def exec_django_cmd(data_params):
    params = data_params.split(",")
    # manage.py here is not used in execute_from_command_line, it is just used to occupy the position.
    command_line_param = ["manage.py"]
    command_line_param.extend(params)
    if not (django_commands_dict is None):
        core_management._commands = django_commands_dict
    core_management.execute_from_command_line(command_line_param)
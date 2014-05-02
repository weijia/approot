# Create your views here.
#from django.template import Context, loader
#from django.contrib.auth.models import User
from django.http import HttpResponse
import sys
import django
from ufs_utils.django_utils import retrieve_param
from django.core.management import execute_from_command_line
from django.contrib.auth import models as auth_models

try:
    from keys.admin_pass import default_admin_password, default_admin_user
except ImportError:
    from keys_template.admin_pass import default_admin_password, default_admin_user

try:
    import django_commands_dict.django_commands_dict as django_commands_dict
except ImportError:
    django_commands_dict = None

import django.core.management as core_management


def cmd(request):
    data = retrieve_param(request)
    import StringIO

    old_out = sys.stdout
    log_out = StringIO.StringIO()
    sys.stdout = log_out

    data_params_ = data["params"]
    params = data_params_.split(",")
    # manage.py here is not used in execute_from_command_line, it is just used to occupy the position.
    command_line_param = ["manage.py"]
    command_line_param.extend(params)
    # The following is for SAE or BAE etc. which does not allow command directory scanning. We must create
    # the commands dict before upload the codes to server
    if not (django_commands_dict is None):
        core_management._commands = django_commands_dict
    execute_from_command_line(command_line_param)

    result = log_out.getvalue()
    sys.stdout = old_out
    return HttpResponse(result.replace("\n", "<br/>"))


def version(request):
    #from objsys.baidu_mail import EmailBackend
    return HttpResponse(django.VERSION)


def create_admin():
    auth_models.User.objects.create_superuser(default_admin_user, 'r@j.cn', default_admin_password)


def handle_create_admin_req(request):
    create_admin()
    return HttpResponse('Done<script>window.href="/"</script>')
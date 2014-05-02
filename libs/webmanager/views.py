# Create your views here.
#from django.template import Context, loader
#from django.contrib.auth.models import User
from django.http import HttpResponse
import sys
import django
from ufs_utils.django_utils import retrieve_param
from django.contrib.auth import models as auth_models
from webmanager.cmd_utils import exec_django_cmd


def cmd(request):
    data = retrieve_param(request)
    import StringIO

    old_out = sys.stdout
    log_out = StringIO.StringIO()
    sys.stdout = log_out

    data_params = data["params"]
    exec_django_cmd(data_params)

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
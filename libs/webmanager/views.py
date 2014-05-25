# Create your views here.
#from django.template import Context, loader
#from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
import sys
import django
from ufs_utils.django_utils import retrieve_param
from django.contrib.auth import models as auth_models, authenticate, login
from cmd_utils import exec_django_cmd
try:
    from keys.admin_pass import default_admin_password, default_admin_user
except ImportError:
    from keys_template.admin_pass import default_admin_password, default_admin_user


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


def login_and_go_home(request):
    data = retrieve_param(request)
    target = data.get("target", "/objsys/homepage/")
    if not request.user.is_authenticated():
        username = data['username']
        password = data['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
    return HttpResponseRedirect(target)
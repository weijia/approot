# Create your views here.
#from django.template import Context, loader
#from django.contrib.auth.models import User
from django.http import HttpResponse
import sys
import django



def index(request):
    import StringIO
    from django.core.management.commands.syncdb import Command as SyncDb
    from django.db import DEFAULT_DB_ALIAS
    saveout = sys.stdout
    log_out = StringIO.StringIO()  
    sys.stdout = log_out
    '''
    try:
        from management import execute_from_command_line
    except:
        from django.core.management import execute_from_command_line

    execute_from_command_line(["manage.py", "syncdb", "--noinput"])
    '''
    #load_initial_data should be False so no directory searching for this command
    SyncDb().handle_noargs(**{"interactive": False, "verbosity": 1, "database": DEFAULT_DB_ALIAS, 'load_initial_data': False})
    result = log_out.getvalue()
    sys.stdout = saveout
    return HttpResponse(result.replace("\n","<br/>"))


def version(request):
    #from objsys.baidu_mail import EmailBackend
    return HttpResponse(django.VERSION)


def create_admin(request):
    #user = User.objects.create_user('richard', 'r@j.cn', 'johnpassword')
    #from django.contrib.auth.create_superuser import createsuperuser
    #createsuperuser()
    from django.contrib.auth import models as auth_models
    auth_models.User.objects.create_superuser('richard', 'r@j.cn', 'johnpassword')
    return HttpResponse('Done<script>window.href="/"</script>')
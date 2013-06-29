import driver_mapping
from models import NetDriver
from django.core.context_processors import csrf
from django.shortcuts import render_to_response, redirect
import os

# Create your views here.
def index(request):
    if request.method == "GET":
        data = request.GET
    else:
        data = request.POST
    s = driver_mapping.sys_driver_mapping()
    existing_mapping = s.get_mapping()
    
    upper_existing_mapping = {}
    for i in existing_mapping:
        upper_existing_mapping[i.upper()] =  existing_mapping[i]
    #print '--------------------------'
    existing_mapping = upper_existing_mapping
    user = None
    passwd = None
    if data.has_key("user"):
        user = data["user"]
    if data.has_key("passwd"):
        passwd = data["passwd"]
    
    #Do map if requested
    for dest in data.keys():
        if (dest == "user") or (dest == "passwd"):
            continue
        #Z:=\\ip\dir or z:=C:\Win
        #No exception, so there is param in requestd
        src = data[dest]
        dest = dest
        print '-----------------', src, dest
        if ("\\\\" in src):
            #net driver
            pass
        else:
            if not os.path.isdir(src):
                src = os.path.dirname(src).upper()
            if not os.path.exists(src):
                print 'local path not exist'
                continue
        #Dummy condition because the original check is not needed anymore
        if True:
            print 'base:'+src
            if existing_mapping.has_key(dest.upper()):
                print dest
                print existing_mapping[dest].upper()
                print src.upper()
                print "'%s'"%existing_mapping[dest]
                print "'%s'"%src
                if existing_mapping[dest.upper()].upper() == src.upper():
                    #Dest already mapped to src, remove the mapping
                    #print existing_mapping
                    s.delete_driver(dest)
                    del existing_mapping[dest]
                    print 'delete driver'
                else:
                    #Dest already mapped to anther, remove the mapping, and add mapping to src
                    s.delete_driver(dest)
                    print 'replace driver'
                    if s.subst_driver(src, dest, user, passwd):
                        existing_mapping[dest.upper()] = src
            else:
                print 'not existing mapping', src, dest
                if s.subst_driver(src, dest, user, passwd):
                    print 'add driver', src, dest, user, passwd
                    existing_mapping[dest.upper()] = src
        else:
            print "driver already mapped", src, dest
    #Save remote path if not exist
    for dest in existing_mapping:
        src = existing_mapping[dest.upper()]
        if 0 == NetDriver.objects.filter(remote = src).count():
            NetDriver(remote = src, local = dest, access_cnt = 1).save()
    is_mapped = []
    qs = NetDriver.objects.all()
    res = []
    
    class MappedItem:
        def __init__(self, local, remote, existing):
            self.local = local
            self.remote = remote
            self.existing = existing

    
    for i in qs:
        print i
        if existing_mapping.has_key(i.local.upper()):
            if existing_mapping[i.local.upper()] == i.remote:
                res.append(MappedItem(i.local.upper(), i.remote, True))
                continue
        res.append(MappedItem(i.local.upper(), i.remote, False))
    
    
    
    c = {"user": request.user, 'all_mapping': res}

    c.update(csrf(request))
    return render_to_response('win_smb/win_smb.html', c)

        
from objsys.tree import register_menu
from models import NetDriver
from django.contrib import admin
from guardian.admin import GuardedModelAdmin

class NetDriverAdmin(GuardedModelAdmin):
    pass

admin.site.register(NetDriver, NetDriverAdmin)


register_menu(u'mapping_driver', u'mapping driver', u'/')


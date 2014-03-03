from models import StaticFile
from django.contrib import admin
from guardian.admin import GuardedModelAdmin

class StaticFileAdmin(GuardedModelAdmin):
    pass
    

admin.site.register(StaticFile, StaticFileAdmin)


#from normal_admin.admin import user_admin_site

#user_admin_site.register(UfsObj)
#user_admin_site.register(CollectionItem, CollectionItemAdmin)

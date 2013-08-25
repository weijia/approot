from django.contrib import admin

from libs.objsys.models import UfsObj
from libs.objsys.models import CollectionItem
from guardian.admin import GuardedModelAdmin


class CollectionItemAdmin(GuardedModelAdmin):
    pass


admin.site.register(UfsObj)
admin.site.register(CollectionItem, CollectionItemAdmin)


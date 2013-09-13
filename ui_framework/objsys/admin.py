from django.contrib import admin

from objsys.models import UfsObj
from objsys.models import Description
from objsys.models import CollectionItem
from guardian.admin import GuardedModelAdmin


class CollectionItemAdmin(GuardedModelAdmin):
    pass


admin.site.register(UfsObj)
admin.site.register(Description)
admin.site.register(CollectionItem, CollectionItemAdmin)


from django.contrib import admin

from objsys.models import UfsObj
from objsys.models import Description
from guardian.admin import GuardedModelAdmin
from collection_management.models import CollectionItem


class CollectionItemAdmin(GuardedModelAdmin):
    pass


admin.site.register(UfsObj)
admin.site.register(Description)
admin.site.register(CollectionItem, CollectionItemAdmin)


from models import UfsObj
from models import CollectionItem
from objsys.tree import register_menu, get_item_id
from django.contrib import admin

from guardian.admin import GuardedModelAdmin


class CollectionItemAdmin(GuardedModelAdmin):
    pass


admin.site.register(UfsObj)
admin.site.register(CollectionItem, CollectionItemAdmin)


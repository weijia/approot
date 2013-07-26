from models import UfsObj
from models import CollectionItem
from ui_framework.objsys.tree import register_menu, get_item_id
from django.contrib import admin

from guardian.admin import GuardedModelAdmin

class CollectionItemAdmin(GuardedModelAdmin):
    pass

register_menu(u'connection', u'processor creator')
register_menu(u'objsys/listing', u'object listing')

admin.site.register(UfsObj)
admin.site.register(CollectionItem, CollectionItemAdmin)


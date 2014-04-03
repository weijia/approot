from collection_management.tree import register_menu
from models import Connection, Processor
from django.contrib import admin
from guardian.admin import GuardedModelAdmin
from utils.string_tools import quote_unicode


class ConnectionAdmin(GuardedModelAdmin):
    pass


register_menu(u'connection/', u'processor creator')
register_menu(u'object_filter/?query_base='+quote_unicode(u'/connection/diagram_list/'), u'diagram management')
register_menu(u'/object_filter/table/?descriptor=service', u'service management')


class ProcessorAdmin(GuardedModelAdmin):
    pass


admin.site.register(Connection, ConnectionAdmin)
admin.site.register(Processor, ProcessorAdmin)


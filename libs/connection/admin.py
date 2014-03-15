from models import Connection, Processor

from django.contrib import admin

from guardian.admin import GuardedModelAdmin
from objsys.tree import register_menu


class ConnectionAdmin(GuardedModelAdmin):
    pass

import utils.string_tools as string_tools

register_menu(u'connection/', u'processor creator')
register_menu(u'object_filter/?query_base='+string_tools.quote_unicode(u'/connection/diagram_list/'), u'diagram management')
register_menu(u'/object_filter/table/?descriptor=service', u'service management')


class ProcessorAdmin(GuardedModelAdmin):
    pass


admin.site.register(Connection, ConnectionAdmin)
admin.site.register(Processor, ProcessorAdmin)


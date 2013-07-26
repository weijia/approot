from models import Connection, Processor

from django.contrib import admin

from guardian.admin import GuardedModelAdmin
from ui_framework.objsys.tree import register_menu


class ConnectionAdmin(GuardedModelAdmin):
    pass

import libs.utils.string_tools as string_tools

register_menu(u'connection/', u'processor creator')
register_menu(u'object_filter/?query_base='+string_tools.quote_unicode(u'/connection/diagram_list/'), u'diagram management')


class ProcessorAdmin(GuardedModelAdmin):
    pass


admin.site.register(Connection, ConnectionAdmin)
admin.site.register(Processor, ProcessorAdmin)


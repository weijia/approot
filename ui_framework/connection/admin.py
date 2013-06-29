from models import Connection, Processor

from django.contrib import admin

from guardian.admin import GuardedModelAdmin

class ConnectionAdmin(GuardedModelAdmin):
    pass
    
    
class ProcessorAdmin(GuardedModelAdmin):
    pass

admin.site.register(Connection, ConnectionAdmin)
admin.site.register(Processor, ProcessorAdmin)


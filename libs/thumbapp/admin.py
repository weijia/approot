from models import ThumbCache
from django.contrib import admin
from guardian.admin import GuardedModelAdmin

class ThumbCacheAdmin(GuardedModelAdmin):
    pass
    

admin.site.register(ThumbCache, ThumbCacheAdmin)



from django.core.management.base import BaseCommand  
from django import db  
  
class Command(BaseCommand):  
    help = 'Output SQL for migration'  
  
    def handle(self, *app_labels, **options):  
        # assumes DEBUG is True in settings  
        db.reset_queries()  
  
        from django.core.management import call_command  
        #kw = {'db-dry-run': 1,  'verbosity': 0}
        options["db-dry-run"] = 1
        options["verbosity"] = 0
        #call_command('migrate objsys 0005_auto__add_field_ufsobj_ufs_obj_type', **kw)
        call_command("migrate", **options)

        for query in db.connection.queries:  
            print query['sql']
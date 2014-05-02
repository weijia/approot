from django.core.management.base import BaseCommand, CommandError
import django.core.management as core_management


class Command(BaseCommand):
    args = ''
    help = 'Create command cache for environment where os.listdir is not working'

    def handle(self, *args, **options):
        print "django_commands_dict =", core_management._commands
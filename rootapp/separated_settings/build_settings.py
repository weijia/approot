import os
RUNNING_PATH = os.path.abspath(os.getcwd())
TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(RUNNING_PATH, 'templates'),   # The comma is a must as otherwise, it will not be treated as a set?
)

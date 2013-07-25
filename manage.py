#!/usr/bin/env python
import os
import sys
from libs.services.svc_base.gui_service import GuiService

pwd = os.getcwd()
sys.path.insert(0, os.path.join(pwd, "libs"))


import os
import sys
unbuffered_out = os.fdopen(os.dup(sys.stdout.fileno()), 'w', 0)
sys.stdout = unbuffered_out
unbuffered_err = os.fdopen(os.dup(sys.stderr.fileno()), 'w', 0)
sys.stderr = unbuffered_err


if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "rootapp.settings")

    if False:  # try:
        from django.core.management import execute_from_command_line
    else:   # except:
        from management import execute_from_command_line

    #gui = GuiService()
    #gui.put({"command": "notify",
    #                  "msg": "Starting background service"})
    execute_from_command_line(sys.argv)

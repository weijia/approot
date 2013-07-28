__author__ = 'Administrator'

import libsys
from libs.services.svc_base.gui_service import GuiService


class Launcher(object):
    def start_app_with_name_no_wait(self, app_name, param_list = []):
        GuiService().put({"command": "LaunchApp", "app_name": app_name, "param": param_list})


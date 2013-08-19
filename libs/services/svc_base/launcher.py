import os

__author__ = 'Administrator'

import libsys
from libs.services.svc_base.gui_service import GuiService


class Launcher(object):
    def start_app_with_name_param_list_with_session_no_wait(self, app_name, param_list=[]):
        """
        Only app's name should be specified, even the extension will not be included in app_name
        :param app_name:
        :param param_list:
        :return:
        """
        GuiService().put({"command": "LaunchApp", "app_name": app_name, "param": param_list})

    def start_app_with_same_filename_with_param_dict(self, app_full_path, param_dict):
        param = []
        for i in param_dict:
            param.append('--%s' % i)
            param.append('%s' % (param_dict[i]))
        self.start_app_with_name_param_list_with_session_no_wait(get_app_name_from_full_path(app_full_path), param)
        return "done"

    def start_app_with_exact_full_path_and_param_list_no_wait(self, exact_full_path, param_list):
        gui_service = GuiService()
        gui_service.addItem({"command": "Launch", "path": exact_full_path, "param": param_list})


def get_app_name_from_ufs_url(app_ufs_url):
    return get_app_name_from_full_path(app_ufs_url)


def get_app_name_from_full_path(app_path):
    app_filename = os.path.basename(app_path)
    app_name = app_filename.split(".")[0]
    return app_name
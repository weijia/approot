import os
from libtool.filetools import find_callable_in_app_framework
from iconizer_main import Iconizer


class Launcher(object):
    @staticmethod
    def start_app_with_name_param_list_no_wait(app_name, param_list=[]):
        """
        Only app's name should be specified, even the extension will not be included in app_name
        :param app_name:
        :param param_list:
        :return:
        """
        app_path = find_callable_in_app_framework(app_name)
        #print app_path
        app_path_and_param = [app_path, ]
        app_path_and_param.extend(param_list)
        #print app_path_and_param
        #print {app_name: app_path_and_param}
        Iconizer().execute({app_name: app_path_and_param})

    @staticmethod
    def start_app_with_same_filename_with_param_dict_no_wait(app_full_path, param_dict):
        param = []
        for i in param_dict:
            param.append('--%s' % i)
            param.append('%s' % (param_dict[i]))
        Launcher.start_app_with_name_param_list_no_wait(get_app_name_from_full_path(app_full_path), param)
        return "done"

    @staticmethod
    def start_app_with_exact_full_path_and_param_list_no_wait(exact_full_path, param_list):
        Iconizer().execute({exact_full_path, [exact_full_path].extend(param_list)})


def get_app_name_from_ufs_url(app_ufs_url):
    return get_app_name_from_full_path(app_ufs_url)


def get_app_name_from_full_path(app_path):
    app_filename = os.path.basename(app_path)
    app_name = app_filename.split(".")[0]
    return app_name
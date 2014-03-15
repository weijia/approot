#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os


def find_root_path(file_path, root_folder_name):
    folder_name = None
    while folder_name != root_folder_name:
        folder_name = os.path.basename(file_path)
        file_path = os.path.dirname(file_path)
    return os.path.abspath(os.path.join(file_path, root_folder_name))


def include_root_path(file_path, root_folder_name):
    include(find_root_path(file_path, root_folder_name))


def include_sub_folder(file_path, root_folder_name, folder_name):
    root_folder_path = find_root_path(file_path, root_folder_name)
    include_in_folder(root_folder_path, folder_name)


def find_root_path_from_pkg(package_info):
    return find_root_path(package_info.file_path, package_info.package_root_name)


def include_sub_folder(package_info, folder_name):
    root_folder_path = find_root_path(package_info)
    include_in_folder(root_folder_path, folder_name)


def include_folders(lib__full_path_list):
    for i in lib__full_path_list:
        include(i)


def get_file_folder(file_path):
    folder = os.path.abspath(os.path.dirname(file_path))
    return folder


def include_file_sibling_folder(file_path, sub_folder_name):
    if (file_path[-1] == "/") or (file_path[-1] == "\\"):
        file_path = file_path[0:-1]
    folder = get_file_folder(file_path)
    include_in_folder(folder, sub_folder_name)


def include_file_folder(file_path):
    include(os.path.dirname(file_path))


def include(folder):
    folder = os.path.abspath(folder)
    if not (folder in sys.path):
        sys.path.insert(0, folder)


def include_in_folder(folder, sub_folder_name):
    include(os.path.join(folder, sub_folder_name))


def exclude(folder):
    folder = os.path.abspath(folder)
    if folder in sys.path:
        sys.path.remove(folder)
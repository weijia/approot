import os
import sys


def include_file_sibling_folder(file_path, sub_folder_name):
    if (file_path[-1] == "/") or (file_path[-1] == "\\"):
        file_path = file_path[0:-1]
    folder = os.path.abspath(os.path.dirname(file_path))
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
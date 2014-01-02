import os


def get_folder(file_path):
    return os.path.abspath(os.path.dirname(file_path))
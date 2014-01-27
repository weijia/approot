import os


def get_folder(file_path):
    return os.path.abspath(os.path.dirname(file_path))


def get_parent_folder(file_path):
    #print "parent:"+os.path.abspath(os.path.join(os.path.dirname(file_path),".."))
    return os.path.abspath(os.path.join(os.path.dirname(file_path),".."))
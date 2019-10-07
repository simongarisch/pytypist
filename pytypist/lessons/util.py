import os


def list_folder_paths():
    """ Returns a list of all folders in this directory
        that do not start with '_'.
    """
    folder_paths = []
    dire_path = os.path.dirname(os.path.realpath(__file__))
    for item in os.listdir(dire_path):
        full_path = os.path.join(dire_path, item)
        if os.path.isdir(full_path) and not item.startswith("_"):
            folder_paths.append(full_path)
    return folder_paths


def list_files(folder_path, endswith=None):
    """ Returns a list of files in this folder. """
    files_list = []
    folder_items = os.listdir(folder_path)
    for item in folder_items:
        include_file = True
        if endswith is not None and not item.endswith(str(endswith)):
            include_file = False
        if include_file:
            file_path = os.path.join(folder_path, item)
            files_list.append(file_path)
    return files_list

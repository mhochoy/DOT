import os


def check_dir(path: str):
    if os.getcwd() != path:
        raise Exception("Directories do not match.")


def is_file(path: str):
    if os.path.isfile(path):
        return True
    return False

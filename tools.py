import os
import shutil


def create_folder(name):
    if not os.path.isdir(name):
        os.mkdir(name)


def move_file(name, to_path):
    shutil.move(name, f"{to_path}/{name}")
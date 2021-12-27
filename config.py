import json
import os
from typing import Set
from security import check_dir
from errors import QuitInterrupt


def read_config():
    preferences: Set[dict]
    try:
        with open('preferences.txt', 'r') as f:
            preferences = json.load(fp=f)

        return preferences
    except FileNotFoundError as e:
        print("No preferences found. Skipping...    ")


def set_config(self):
    user_path: str = input("Path:   ")
    if user_path == "q" or user_path == "quit":
        raise QuitInterrupt
    if "dotext" == user_path:
        # Custom Extension Handling
        return
    if f'{user_path[0]}:\\Windows' in user_path or "C:\\" == user_path:
        raise Exception("Cannot edit Windows directory.")
    if user_path != "":
        try:
            os.chdir(user_path)
            configuration: Config = Config(path=user_path)
            check_dir(path=configuration.path)
        except Exception as e:
            print(e)
            self.set_config()

    return configuration


class Config:
    audio: str = "Audio"
    application: str = "Applications"
    text: str = "Text"
    image: str = "Images"
    video: str = "Videos"
    folders: dict = {"audio": audio,
                     "application": application,
                     "text": text,
                     "image": image,
                     "video": video}
    type_filter: list = []

    # Extension Handling
    extension_filter: list = []
    custom_extension_folders: dict = {'rdp': "My Custom Folder",
                                      'pdf': "Documents",
                                      'url': "Shortcuts",
                                      'flp': "FLPs",
                                      'reg': "Registry Files",
                                      'fbx': "Models",
                                      'zip': "ZIP Files",
                                      'rar': "RAR Files",
                                      'unitypackage': "Unity Packages",
                                      'torrent': "Torrents"}

    def __init__(self, path):
        if path is None:
            return
        self.path: str = path

    def set_path(self, new_path):
        self.path = new_path

    def get_path(self):
        return self.path

    def get_folder_name(self, name: str):
        return self.folders.get(name)

    def get_custom_folder(self, name: str):
        return self.custom_extension_folders.get(name)

    def add_type_filter(self, file_type: str):
        if file_type not in self.folders.keys():
            return
        return self.type_filter.append(file_type)


def write_config(config: Config is None):
    if config is None:
        return
    preferences = {
        config.folders,
        config.custom_extension_folders
    }
    with open('preferences.txt', 'w') as f:
        json.dump(preferences, f)
        f.close()

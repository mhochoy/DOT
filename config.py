import json
import os
from typing import Set
from security import check_dir


def set_config(self):
    user_path: str = input()
    if user_path != "":
        configuration: Config = Config(path=user_path)
        os.chdir(user_path)
        try:
            check_dir(path=configuration.path)
        except Exception as e:
            print(e)
            self.set_config()

    return configuration


class Config:
    audio: str = "Audio"
    application: str = "Applications"
    text: str = "Text"
    image: str = "Image"
    video: str = "Videos"
    folders: dict = {"audio": audio,
                     "application": application,
                     "text": text,
                     "image": image,
                     "video": video}
    type_filter: list = []

    # Extension Handling
    extension_filter: list = []
    custom_extension_folders: dict = {'rdp': "My Custom Folder"}

    def __init__(self, path):
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

    def write_config(self):
        preferences: Set[dict] = {
            self.folders,
            self.custom_extension_folders
        }
        with open('preferences.txt', 'w') as f:
            json.dump(preferences, f)
            f.close()

    def read_config(self):
        with open('preferences.txt', 'r') as f:
            preferences = json.load(fp=f)

        print(preferences)

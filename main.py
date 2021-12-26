from config import set_config, Config, read_config, write_config
from security import is_file
from errors import FileError, QuitInterrupt, parse_magic_io_error
from tools import move_file, create_folder
import magic
import os

by_type: bool = True
configuration = None
preferences = False


def app():
    try:
        configuration: Config = get_preferences()
        for raw_file_name in os.listdir(path="."):
            file: str
            if is_file(raw_file_name):
                try:
                    file = magic.from_file(filename=raw_file_name, mime=True)
                    if 'cannot open' in file:
                        raise FileError(file)
                    else:
                        # Move files to suggested path
                        file = file.split('/')[0]
                        extension: str = raw_file_name.split(".")[1]
                        # User must add file to custom extension folder
                        print("Unmoved: ", file, f"Extension: .{extension}")
                        folder: str = configuration.get_custom_folder(name=extension) \
                            if configuration.get_custom_folder(name=extension) != '' \
                            else configuration.get_folder_name(name=file)
                        if folder:
                            print(raw_file_name + " to :" + folder + f" [Extension: .{extension}]")
                            create_folder(name=folder)
                            move_file(name=raw_file_name, to_path=folder)
                except PermissionError as e:
                    print("Permission denied for the following file:    " + e.filename)
                except FileError as e:
                    print("The following file could not be accessed:     " + parse_magic_io_error(err=e.message))
                except FileNotFoundError as e:
                    print("The path could not be found:     ", e.filename)
                    app()

            else:
                pass
        app()
    except AttributeError as e:
        print("Config not set. Restarting...    ")
        app()
    except QuitInterrupt as e:
        quit_app()


def get_preferences():
    config: Config
    saved_config: Config = read_preferences()
    if saved_config:
        config = saved_config
    else:
        config = set_config(self=Config)

    return config


def read_preferences():
    config: Config = read_config()
    if config:
        return config


def quit_app():
    if configuration is not None:
        write_config(config=configuration)
    print("Quiting...")
    quit()

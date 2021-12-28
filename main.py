from config import set_config, Config, read_config, write_config
from security import is_file
from errors import FileError, QuitInterrupt, parse_magic_io_error
from tools import move_file, create_folder
import magic
import os

configuration = None


def app():
    try:
        configuration: Config = get_preferences()
        organize_files(config=configuration)
        app()
    except QuitInterrupt:
        quit_app()
    except Exception as e:
        print(f"Could not set configuration for the following reason:    {e}")
    except AttributeError:
        print("Config not set. Restarting...    ")
        app()


def organize_files(config: Config):
    for raw_file_name in os.listdir(path="."):
        file_type: str
        if is_file(raw_file_name):
            try:
                file_type = magic.from_file(filename=raw_file_name, mime=True)
                if 'cannot open' in file_type:
                    raise FileError(file)
                else:
                    file_type = file_type.split('/')[0]
                    extension: str = raw_file_name.split(".")[-1]
                    # Get the default folder name if there is no custom folder set up for the file type
                    folder: str = config.get_custom_folder(name=extension) \
                        if config.get_custom_folder(name=extension) \
                        else config.get_folder_name(name=file_type)
                    if folder:
                        print(raw_file_name + " to :" + folder + f" [Extension: .{extension}]")
                        create_folder(name=folder)
                        move_file(name=raw_file_name, to_path=folder)
                    else:
                        # User must add file to custom extension folder
                        print("Unmoved: ", file_type, f"{raw_file_name} - Extension: .{extension}")

            except PermissionError as e:
                print("Permission denied for the following file:    " + e.filename)
            except FileError as e:
                print("The following file could not be accessed:     " + parse_magic_io_error(err=e.message))
            except FileNotFoundError as e:
                print("The path could not be found:     ", e.filename)
                app()
            except UnicodeDecodeError as e:
                print("Ran into unsupported file name.   ", e)

        else:
            pass


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

import re


class FileError(Exception):
    def __init__(self, msg):
        self.message = msg
        pass


class QuitInterrupt(Exception):
    def __init__(self):
        pass


def parse_magic_io_error(err):
    # Regular expressions for filename and file-type parsing from Magic errors
    fn = re.search(r"`\w+[a-z A-Z]\w+", err)
    file_type = re.search(r"\.\w+[a-zA-Z0-9]", err)
    # Filename with extension
    file = fn.group(0)[1::] + file_type.group(0)
    return file

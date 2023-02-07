import os


def check_if_file_exists(file_path):
    found = False

    try:
        os.stat(file_path)
        found = True

    except OSError:
        pass

    return found

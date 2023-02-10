import os


def check_if_file_exists(file_path):
    found = False

    try:
        os.stat(file_path)
        found = True

    except OSError:
        pass

    return found


def get_file_content(file_path):
    file_content = ""

    if check_if_file_exists(file_path):
        with open(file_path, "r") as file:
            file_content = file.read()

    return file_content

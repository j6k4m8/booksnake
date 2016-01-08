import os


def convert_epub(filename):
    return os.system("kindlegen " + filename)


def get_file_extension(filename):
    return filename.split('.')[1:][0]

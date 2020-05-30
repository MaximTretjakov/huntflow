from os import listdir
from os.path import isfile, join, basename

path_to = '/home/maxim/projects/huntflow/resume/'


def get_resume_file(target, path):
    files = [path_to + file_ for file_ in listdir(path) if isfile(join(path, file_))]
    for file_path in files:
        if target in basename(file_path):
            return file_path

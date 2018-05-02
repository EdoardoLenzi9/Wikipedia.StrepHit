import os

def log(file, text, access_method = 'ab+'):
    with open(file, access_method) as f:
        f.write("{0}\n".format(text))

def exists(file):
    return os.path.isfile(file)
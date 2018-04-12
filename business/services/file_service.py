import os

def log(file, text):
    with open(file, 'ab+') as f:
        f.write("{0}\n".format(text))

def exists(file):
    return os.path.isfile(file)
import os
from shutil import copyfile

BACKUP_EXTENSION = "backup"

def log(file, text, access_method = 'ab+'):
    with open(file, access_method) as f:
        f.write("{0}\n".format(text))

def exists(file):
    return os.path.isfile(file)

def copy(source, destination):
    copyfile(source, destination)

def remove(source):
    os.remove(source)

def backup(source):
    try :
        copy(source, "{0}.{1}".format(source, BACKUP_EXTENSION))
    except :
        print("copy error, file not found: {0}".format(source))


def restore(source):
    backup_file = "{0}.{1}".format(source, BACKUP_EXTENSION)
    try :
        if exists(source) : 
            remove(source)
        copyfile(backup_file, source)
        os.remove(backup_file)
    except :
        print("restore error with file: {0}".format(source))


def rename(old, new):
    os.rename(old, new)

def fast_backup(source):
    backup_file = "{0}.{1}".format(source, BACKUP_EXTENSION)
    try :
        rename(source, backup_file)
    except :
        print("fast_backup error, file not found: {0}".format(source))

def fast_restore(source):
    backup_file = "{0}.{1}".format(source, BACKUP_EXTENSION)
    try :
        if exists(source) : 
            remove(source)
        rename(backup_file, source)
    except :
        print("fast_restore error, file not found: {0}".format(source))

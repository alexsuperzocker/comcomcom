from os import listdir
from os.path import isfile, join
from ntpath import basename

def pick_file(msg="Please enter the path of a file:\n"):
    usr_path = ""
    while(not isfile(usr_path)):
        usr_path = input(msg)
    return usr_path

def get_file_name(path):
    return basename(path).split(".")[0]

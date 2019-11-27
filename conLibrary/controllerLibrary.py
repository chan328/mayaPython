from maya import cmds
import  os
import json
import pprint

USERAPPDIR = cmds.internalVar(userAppDir=True)
DIRECTORY = os.path.join(USERAPPDIR, 'controllerLibrary')
# mac, windows => \\\ / linux => \\\\

def createDirectory(directory=DIRECTORY):
    """'
    Creates the given directory if it's doesn't exist already
    :param directory(str): the directory to create


    """
    if not os.path.exists(directory):
        os.mkdir(directory)
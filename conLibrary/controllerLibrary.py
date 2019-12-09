from maya import cmds
from operator import eq
import os
import json


USERAPPDIR = cmds.internalVar(userAppDir=True)
DIRECTORY = os.path.join(USERAPPDIR, 'controllerLibrary')
# mac, windows => \\\ / linux => \\\\


def create_directory(directory=DIRECTORY):
    """'
    Creates the given directory if it's doesn't exist already
    :param directory(str): the directory to create


    """
    if not os.path.exists(directory):
        os.mkdir(directory)


class ControllerLibrary(dict):

    def save(self, name, directory=DIRECTORY, screenshot=True, **info):
        files = os.listdir(directory)
        maya_files = [f for f in files if f.endswith('.ma')]
        for ma in maya_files:
            if eq(ma, name+".ma"):
                raise NameError("There is already same name in files. Please use other name or delete that file.")

        create_directory(directory)

        path = os.path.join(directory, '%s.ma' % name)
        info_file = os.path.join(directory, '%s.json' % name)

        info['name'] = name
        info['path'] = path

        cmds.file(rename=path)

        if cmds.ls(selection=True):
            cmds.file(force=True, type='mayaAscii', exportSelected=True)
        else:
            cmds.file(save=True, type='mayaAscii', force=True)

        if screenshot:
            info['screenshot'] = self.save_screenshot(name, directory=directory)

        # with command is safe way to open file
        with open(info_file, 'w') as f:
            json.dump(info, f, indent=4)

        self[name] = path
        # updating every time when you saved

    def find(self, directory=DIRECTORY):
        """
        find controller on disk
        :param directory: the dict to serach in
        :return:
        """
        self.clear()
        if not os.path.exists(directory):
            return

        files = os.listdir(directory)
        maya_files = [f for f in files if f.endswith('.ma')]
        # same as below code <List Comprehension>
        # for f in files:
        #   if f.endwiths('.ma') ~~

        for ma in maya_files:
            name, extention = os.path.splitext(ma)
            path = os.path.join(directory, ma)

            info_file = '%s.json' % name
            if info_file in files:
                info_file = os.path.join(directory, info_file)

                with open(info_file, 'r') as f:
                    info = json.load(f)
            else:
                info = {}

            screenshot = '%s.jpg' % name
            default_screenshot = 'C:\\Users\\Chan\\Documents\\maya\\2018\\scripts\\image\\defaultimage.jpg'
            if screenshot in files:
                info['screenshot'] = os.path.join(directory, name)
            else:
                # if screenShot doesn't exist use default image
                info['screenshot'] = default_screenshot

            info['name'] = name
            info['path'] = path

            self[name] = info

    def load(self, name):
        path = self[name]['path']
        cmds.file(path, i=True, usingNamespaces=False)

    def save_screenshot(self, name, directory=DIRECTORY):
        path = os.path.join(directory, '%s.jpg' % name)
        cmds.viewFit()
        cmds.setAttr('defaultRenderGlobals.imageFormat', 8)
        # in maya jpeg imageformat is 8

        cmds.playblast(completeFilename=path, forceOverwrite=True, format='image', width=200, height=200,
                       showOrnaments=False, startTime=1, endTime=1, viewer=False)

        return path
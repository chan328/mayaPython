# Try this in Maya before starting to run script in PyCharm:
# import maya.cmds as cmds
# if not cmds.commandPort(':4434', q=True):
#    cmds.commandPort(n=':4434')

import maya.cmds as cmds

class Gear(object):
    def __init__(self):
        self.shape = None
        self.transform = None
        self.constructor = None
        self.extrude = None

    def create(self, teeth=10, length=0.3):
        spans = teeth * 2

        self.createPipe(spans)

        self.makeTeeth(teeth=teeth, length=length)

    def createPipe(self, spans):
        self.transform, self.shape = cmds.polyPipe(subdivisionAxis=spans)
        if(self.transform is None):
            print("self.transform is None")

        for node in cmds.listConnections('%s.inMesh' % self.transform):
            if cmds.objectType(node) == 'polyPipe':
                self.constructor = node
                break

    def makeTeeth(self, teeth=10, length=0.3):
        cmds.select(clear=True)
        faces = self.getTeethFaces(teeth)
        for face in faces:
            cmds.select('%s.%s' % (self.transform, face), add=True)

        self.extrude = cmds.polyExtrudeFacet(localTranslateZ=length)[0]
        cmds.select(clear=True)

        cmds.polyExtrudeFacet(self.extrude, edit=True, ltz=length)

    def changeTeeth(self, teeth=10, length=0.3):
        cmds.polyPipe(self.constructor, edit=True, sa=teeth * 2)
        self.modifyExtrude(teeth=teeth, length=length)

    def getTeethFaces(self, teeth):
        spans = teeth * 2
        sideFaces = range(spans*2, spans*3, 2)

        faces = []
        for face in sideFaces:
            faces.append('f[%d]' % face)

        return faces

    def modifyExtrude(self, teeth=10, length=0.3):
        faces = self.getTeethFaces(teeth)
        cmds.setAttr('%s.inputComponents' % self.extrude, len(faces), *faces, type='componentList')

        self.changeTeeth(length)
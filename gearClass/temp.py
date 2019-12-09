# Try this in Maya before starting to run script in PyCharm:
# import maya.cmds as cmds
# if not cmds.commandPort(':4434', q=True):
#    cmds.commandPort(n=':4434')
import maya.cmds as cmds

def createGear(teeth=10, length=0.3):
    """
    :param teeth: the number of teeth to create
    :param length: the length of the teech
    :return: A tuple of the transform, constructor and extrude node
    """
    # teeth are every alternate face, so spans X 2
    spans = teeth * 2

    transfrom, constructor = cmds.polyPipe(subdivisionsAxis=spans)
    # side faces goes 40, 42, 44, 46, 48, 50, 52 ...
    sideFaces = range(spans * 2, spans * 3, 2)

    cmds.select(clear=True)

    for face in sideFaces:
        cmds.select('%s.f[%s]' % (transfrom, face), add=True)

    extrude = cmds.polyExtrudeFacet(localTranslateZ=length)[0]
    return transfrom, constructor, extrude


def changeTeeth(constructor, extrude, teeth=10, length=0.3):
    spans = teeth * 2

    cmds.polyPipe(constructor, edit=True,
                  # edit : flag that is knows and sort of creating a new one to edit the existing
                  subdivisionsAxis=spans)

    sideFaces = range(spans*2, spans*3, 2)
    faceNames = []

    # [u'f[40]', u'f[42]' ... ]

    for face in faceNames:
        faceName = 'f[%s]' % (face)
        faceNames.append(faceName)

    cmds.setAttr('%s.inputComponents' % (extrude),
                 len(faceNames),
                 *faceNames,
                 type="componentList")

    cmds.polyExtrudeFacet(extrude, edit=True, ltz=length)




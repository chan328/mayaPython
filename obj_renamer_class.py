from maya import cmds

SUFFIX = {"mesh": "geo",
                  "joint": "jnt",
                  "camera": None}

DEFULAT = "grp"

class obj_reamer(object):
    def rename(self, selection=False):
        objects = cmds.ls(selection=selection, dag=True)

        if selection and not objects:
            raise RuntimeError("you don't have anything selected")

        objects.sort(key=len, reverse=True)

        for obj in objects:
            shortName = obj.split('|')[-1]
            children = cmds.listRelatives(obj, children=True) or []
            if len(children) == 1:
                child = children[0]
                objType = cmds.objectType(child)
            else:
                objType = cmds.objectType(obj)

            suffix = SUFFIX.get(objType, DEFULAT)


from maya import cmds

def tween(percentage, obj=None, attrs=None, selection=True):
    # if obj is not given and selection set to false, error occure
    if not obj and not selection:
        raise ValueError("No object given to tween")

    # if you got this error, you didn't select any obj in maya
    # Error: IndexError: file C:/Users/Chan/Documents/maya/2018/scripts\tweenerUI.py line 9: list index out of range
    if not obj:
        obj = cmds.ls(selection=True)[0]

    if not attrs:
        attrs = cmds.listAttr(obj, keyable=True)
    # attrs value
    # [u'visibility', u'translateX', u'translateY', u'translateZ', u'rotateX', u'rotateY', u'rotateZ', u'scaleX', u'scaleY', u'scaleZ']

    currentTime = cmds.currentTime(query=True)
    print(obj)

    for attr in attrs:

        attrFull = '%s.%s' % (obj, attr)
        # many maya command require full name so when you use maya command with obj name, you'll need full name
        # for example, 'pCube1.visibility' 'pCube1.translateX'
        keyframes = cmds.keyframe(attrFull, query=True)

        # if there no keyframes, then continue
        if not keyframes:
            continue

        previous_keyframes = []
        later_keyframes = []
        for k in keyframes:
            if k < currentTime:
                previous_keyframes.append(k)
            elif k > currentTime:
                later_keyframes.append(k)
        # later_keyframes = [frame for frame in keyframes if frame > currentTime]
        # this code is exactly same as upper code. but it's more faster

        if not previous_keyframes and not later_keyframes:
            continue

        if previous_keyframes:
            previous_keyframe = max(previous_keyframes)
        else:
            previous_keyframe = None

        # else None == else : nextframe = None
        nextframe = min(later_keyframes) if later_keyframes else None

        if not previous_keyframe or not nextframe:
            continue

        previous_value = cmds.getAttr(attrFull, time=previous_keyframe)
        next_value = cmds.getAttr(attrFull, time=nextframe)

        difference = next_value - previous_value
        weight_difference = (difference * percentage) / 100.0
        currentValue = previous_value + weight_difference

        cmds.setKeyframe(attrFull, time=currentTime, value=currentValue)

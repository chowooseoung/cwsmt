import maya.cmds as mc
import maya.api.OpenMaya as om


def maya_useNewAPI():
    pass

class TateLocatorHUDNode(om.MPxNode):
    TYPE_NAME = "tate_locatorHUD"
    TYPE_ID = om.MTypeId(0x77770002)
    
    def __init__(self):
        super(TateLocatorHUDNode, self).__init__()

    @classmethod
    def creator(cls):
        return TateLocatorHUDNode()

    @classmethod
    def initialize(cls):
        pass

def initializePlugin(plugin):

    vendor = "cho wooseoung"
    version = "1.0.0"

    pluginFn = om.MFnPlugin(plugin, vendor, version)

    try:
        pluginFn.registerNode(TateLocatorHUDNode.TYPE_NAME,
                                TateLocatorHUDNode.TYPE_ID,
                                TateLocatorHUDNode.creator,
                                TateLocatorHUDNode.initialize,
                                om.MPxNode.kDependNode)
    except:
        om.MGlobal.displayError("Failed to register node : {0}".format(TateLocatorHUDNode.TYPE_NAME))

def uninitializePlugin(plugin):
    
    pluginFn = om.MFnPlugin(plugin)

    try:
        pluginFn.deregisterNode(TateLocatorHUDNode.TYPE_ID)
    except:
        om.MGlobal.displayError("Failed to deregister node :{0}".format(TateLocatorHUDNode.TYPE_NAME))


if __name__ == "__main__":
    
    mc.file(new=True, force=True)
    plugin_name = "tate_locatorHUD.py"

    mc.evalDeferred("if mc.pluginInfo('{0}', q=True, loaded=True): mc.unloadPlugin('{0}')".format(plugin_name))
    mc.evalDeferred("if not mc.pluginInfo('{0}', q=True, loaded=True): mc.loadPlugin('{0}')".format(plugin_name))

    mc.evalDeferred("mc.createNode('tate_locatorHUD')")
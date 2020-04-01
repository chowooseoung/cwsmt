import maya.cmds as mc
import maya.api.OpenMaya as om

def maya_useNewAPI():
    pass

class TateCurveLengthP(om.MPxNode):

    TYPE_NAME = "tate_curveLengthP"
    TYPE_ID = om.MTypeId(0x77770003)

    inputCurve = None
    inputLength = None
    outputParameter = None

    def __init__(self):
        super(TateCurveLengthP, self).__init__()

    def compute(self, plug, data):
        
        if plug == TateCurveLengthP.outputParameter:

            inputCrv = data.inputValue(TateCurveLengthP.inputCurve).asNurbsCurve()
            inputLen = data.inputValue(TateCurveLengthP.inputLength).asDouble()

            crvFn = om.MFnNurbsCurve(inputCrv)
            outputPValue = crvFn.findLengthFromParam(inputLen)

            outputP = data.inputValue(TateCurveLengthP.outputParameter).asFloat()
            outputP.setDouble(outputPValue)

            data.setClean(plug)

    @classmethod
    def creator(cls):
        return TateCurveLengthP()
    
    @classmethod
    def initialize(cls):
        mtAttr = om.MFnTypedAttribute()
        nuAttr = om.MFnNumericAttribute()

        cls.inputCurve = mtAttr.create("inputCurve", "inputCurve", om.MFnData.kNurbsCurve)
        mtAttr.keyable = True

        cls.inputLength = nuAttr.create("inputLength", "inputLength", om.MFnNumericData.kDouble, 0.0)
        nuAttr.keyable = True

        cls.outputParameter = nuAttr.create("outputParameter", "outputParameter", om.MFnNumericData.kDouble, 0.0)
        nuAttr.writable = False

        cls.addAttribute(cls.inputCurve)
        cls.addAttribute(cls.inputLength)
        cls.addAttribute(cls.outputParameter)
        
        cls.attributeAffects(cls.inputCurve, cls.outputParameter)
        cls.attributeAffects(cls.inputLength, cls.outputParameter)

def initializePlugin(plugin):

    vendor = "cho wooseoung"
    version = "1.0.0"

    pluginFn = om.MFnPlugin(plugin, vendor, version)

    try:
        pluginFn.registerNode(TateCurveLengthP.TYPE_NAME,
                                TateCurveLengthP.TYPE_ID,
                                TateCurveLengthP.creator,
                                TateCurveLengthP.initialize,
                                om.MPxNode.kDependNode)
    except:
        om.MGlobal.displayError("Failed to register node : {0}".format(TateCurveLengthP.TYPE_NAME))

def uninitializePlugin(plugin):
    
    pluginFn = om.MFnPlugin(plugin)

    try:
        pluginFn.deregisterNode(TateCurveLengthP.TYPE_ID)
    except:
        om.MGlobal.displayError("Failed to deregister node : {0}".format(TateCurveLengthP.TYPE_NAME))


if __name__ == "__main__":
    
    mc.file(new=True, force=True)
    plugin_name = "tate_curveLengthP.py"

    mc.evalDeferred("if mc.pluginInfo('{0}', q=True, loaded=True): mc.unloadPlugin('{0}')".format(plugin_name))
    mc.evalDeferred("if not mc.pluginInfo('{0}', q=True, loaded=True): mc.loadPlugin('{0}')".format(plugin_name))

    mc.evalDeferred("mc.createNode('tate_curveLengthP')")
    
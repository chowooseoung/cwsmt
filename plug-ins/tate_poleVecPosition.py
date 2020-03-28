import maya.cmds as mc
import maya.api.OpenMaya as om

def maya_useNewAPI():
    pass

class TatePoleVecPosition(om.MPxNode):

    TYPE_NAME = "tate_poleVecPosition"
    TYPE_ID = om.MTypeId(0x77770001)

    zero_obj = None
    first_obj = None
    second_obj = None
    offset_obj = None
    outputParentInverseMatrix_obj = None

    outputTranslate_obj = None
    outputTX_obj = None
    outputTY_obj = None
    outputTZ_obj = None

    def __init__(self):
        super(TatePoleVecPosition, self).__init__()

    def compute(self, plug, data):

        if plug == TatePoleVecPosition.outputTranslate_obj: 
            
            zeroM = data.inputValue(TatePoleVecPosition.zero_obj).asFloatMatrix()
            zero_point = om.MVector(zeroM[12], zeroM[13], zeroM[14])

            firstM = data.inputValue(TatePoleVecPosition.first_obj).asFloatMatrix()
            first_point = om.MVector(firstM[12], firstM[13], firstM[14])

            secondM = data.inputValue(TatePoleVecPosition.second_obj).asFloatMatrix()
            second_point = om.MVector(secondM[12], secondM[13], secondM[14])

            offset = data.inputValue(TatePoleVecPosition.offset_obj).asDouble()

            project_vec = first_point - zero_point
            target_vec = second_point - zero_point

            output = ((project_vec * target_vec) / (target_vec * target_vec)) * target_vec
            output = zero_point + output 
            output = (first_point - output) + output + (((first_point - output) / (first_point - output).length()) * offset)

            matrix = om.MMatrix()
            matrix.setElement(0, 0, 1)
            matrix.setElement(0, 1, 0)
            matrix.setElement(0, 2, 0)
            matrix.setElement(0, 3, 0)
            
            matrix.setElement(1, 0, 0)
            matrix.setElement(1, 1, 1)
            matrix.setElement(1, 2, 0)
            matrix.setElement(1, 3, 0)
            
            matrix.setElement(2, 0, 0)
            matrix.setElement(2, 1, 0)
            matrix.setElement(2, 2, 1)
            matrix.setElement(2, 3, 0)
            
            matrix.setElement(3, 0, output[0])
            matrix.setElement(3, 1, output[1])   
            matrix.setElement(3, 2, output[2])
            matrix.setElement(3, 3, 1)

            outputParentInverseM = data.inputValue(TatePoleVecPosition.outputParentInverseMatrix_obj).asFloatMatrix()
            finalMatrix = matrix * om.MMatrix(outputParentInverseM)

            translate = om.MTransformationMatrix(finalMatrix).translation(om.MSpace.kWorld)

            outputT = data.outputValue(TatePoleVecPosition.outputTranslate_obj)
            outputT.set3Double(*translate)

            data.setClean(plug)
            
    @classmethod
    def creator(cls):
        return TatePoleVecPosition()
    
    @classmethod
    def initialize(cls):
        matrix_attr = om.MFnMatrixAttribute()
        numeric_attr = om.MFnNumericAttribute()

        cls.zero_obj = matrix_attr.create("zeroMatrix", "zeroMatrix", om.MFnMatrixData.kMatrix)
        matrix_attr.keyable = True
        matrix_attr.readable = False

        cls.first_obj = matrix_attr.create("firstMatrix", "firstMatrix", om.MFnMatrixData.kMatrix)
        matrix_attr.keyable = True
        matrix_attr.readable = False

        cls.second_obj = matrix_attr.create("secondMatrix", "secondMatrix", om.MFnMatrixData.kMatrix)
        matrix_attr.keyable = True
        matrix_attr.readable = False

        cls.offset_obj = numeric_attr.create("offset", "offset", om.MFnNumericData.kDouble, 0.0)
        numeric_attr.keyable = True
        numeric_attr.readable = False
    
        cls.outputParentInverseMatrix_obj = matrix_attr.create("outputParentInverseMatrix", "outputParentInverseMatrix", om.MFnMatrixData.kMatrix)
        matrix_attr.keyable = True
        matrix_attr.readable = False

        cls.outputTX_obj = numeric_attr.create("translateX", "tx", om.MFnNumericData.kDouble, 0.0)
        numeric_attr.keyable = True
        numeric_attr.readable = False
        cls.outputTY_obj = numeric_attr.create("translateY", "ty", om.MFnNumericData.kDouble, 0.0)
        numeric_attr.keyable = True
        numeric_attr.readable = False
        cls.outputTZ_obj = numeric_attr.create("translateZ", "tz", om.MFnNumericData.kDouble, 0.0)
        numeric_attr.keyable = True
        numeric_attr.readable = False
        cls.outputTranslate_obj = numeric_attr.create("outputTranslate", "outputTranslate",
                                                        cls.outputTX_obj, cls.outputTY_obj, cls.outputTZ_obj)
        numeric_attr.writable = False

        cls.addAttribute(cls.zero_obj)
        cls.addAttribute(cls.first_obj)
        cls.addAttribute(cls.second_obj)
        cls.addAttribute(cls.offset_obj)
        cls.addAttribute(cls.outputParentInverseMatrix_obj)
        cls.addAttribute(cls.outputTranslate_obj)

        cls.attributeAffects(cls.zero_obj, cls.outputTranslate_obj)
        cls.attributeAffects(cls.first_obj, cls.outputTranslate_obj)
        cls.attributeAffects(cls.second_obj, cls.outputTranslate_obj)
        cls.attributeAffects(cls.offset_obj, cls.outputTranslate_obj)
        cls.attributeAffects(cls.outputParentInverseMatrix_obj, cls.outputTranslate_obj)

def initializePlugin(plugin):

    vendor = "cho wooseoung"
    version = "1.0.0"

    pluginFn = om.MFnPlugin(plugin, vendor, version)

    try:
        pluginFn.registerNode(TatePoleVecPosition.TYPE_NAME,
                                TatePoleVecPosition.TYPE_ID,
                                TatePoleVecPosition.creator,
                                TatePoleVecPosition.initialize,
                                om.MPxNode.kDependNode)
    except:
        om.MGlobal.displayError("Failed to register node : {0}".format(TatePoleVecPosition.TYPE_NAME))

def uninitializePlugin(plugin):
    
    pluginFn = om.MFnPlugin(plugin)

    try:
        pluginFn.deregisterNode(TatePoleVecPosition.TYPE_ID)
    except:
        om.MGlobal.displayError("Failed to deregister node : {0}".format(TatePoleVecPosition.TYPE_NAME))


if __name__ == "__main__":
    
    mc.file(new=True, force=True)
    plugin_name = "tate_poleVecPosition.py"

    mc.evalDeferred("if mc.pluginInfo('{0}', q=True, loaded=True): mc.unloadPlugin('{0}')".format(plugin_name))
    mc.evalDeferred("if not mc.pluginInfo('{0}', q=True, loaded=True): mc.loadPlugin('{0}')".format(plugin_name))
    
    mc.evalDeferred("node = mc.createNode('tate_poleVecPosition')")

    mc.evalDeferred("zero = mc.sphere(ch=False)[0]")
    mc.evalDeferred("first = mc.sphere(ch=False)[0]")
    mc.evalDeferred("mc.setAttr('{0}.tx'.format(first), 6)")
    mc.evalDeferred("mc.setAttr('{0}.tz'.format(first), -1)")
    mc.evalDeferred("second = mc.sphere(ch=False)[0]")  
    mc.evalDeferred("mc.setAttr('{0}.tx'.format(second), 12)")
    
    mc.evalDeferred("output = mc.sphere(ch=False)[0]")
    mc.evalDeferred("mc.connectAttr('{0}.worldMatrix[0]'.format(zero), '{0}.zeroMatrix'.format(node))")
    
    mc.evalDeferred("mc.connectAttr('{0}.worldMatrix[0]'.format(first), '{0}.firstMatrix'.format(node))")
    
    mc.evalDeferred("mc.connectAttr('{0}.worldMatrix[0]'.format(second), '{0}.secondMatrix'.format(node))")

    mc.evalDeferred("mc.connectAttr('{0}.parentInverseMatrix[0]'.format(output), '{0}.outputParentInverseMatrix'.format(node))")

    mc.evalDeferred("mc.addAttr('{0}'.format(output), ln='offset', at='float', min=0, dv=0, k=1)")
    
    mc.evalDeferred("mc.connectAttr('{0}.offset'.format(output), '{0}.offset'.format(node))")

    mc.evalDeferred("mc.connectAttr('{0}.outputTranslate'.format(node), '{0}.t'.format(output))")
    
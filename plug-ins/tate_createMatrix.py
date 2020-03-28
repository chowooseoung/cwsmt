import maya.cmds as mc
import maya.api.OpenMaya as om

def maya_useNewAPI():
    pass

class TateCreateMatrix(om.MPxNode):

    TYPE_NAME = "tate_createMatrix"
    TYPE_ID = om.MTypeId(0x77770000)

    baseMatrix_obj = None
    vector1Matrix_obj = None
    vector2Matrix_obj = None
    axis_obj = None
    forward_obj = None
    up_obj = None
    outputParentInverseMatrix_obj = None

    outputTranslate_obj = None
    outputTX_obj = None
    outputTY_obj = None
    outputTZ_obj = None

    outputRotate_obj = None
    outputRX_obj = None
    outputRY_obj = None
    outputRZ_obj = None

    def __init__(self):
        super(TateCreateMatrix, self).__init__()

    def compute(self, plug, data):

        if (plug == TateCreateMatrix.outputTranslate_obj) or (plug == TateCreateMatrix.outputRotate_obj): 
            
            baseM = data.inputValue(TateCreateMatrix.baseMatrix_obj).asFloatMatrix()
            base_point = om.MVector(baseM[12], baseM[13], baseM[14])

            forwardM = data.inputValue(TateCreateMatrix.vector1Matrix_obj).asFloatMatrix()
            forward_point = om.MVector(forwardM[12], forwardM[13], forwardM[14])

            upM = data.inputValue(TateCreateMatrix.vector2Matrix_obj).asFloatMatrix()
            up_point = om.MVector(upM[12], upM[13], upM[14])

            x = om.MVector(0,0,0)
            y = om.MVector(0,0,0)
            z = om.MVector(0,0,0)
            t = om.MVector(0,0,0)

            axis = data.inputValue(TateCreateMatrix.axis_obj).asShort()
            forward = data.inputValue(TateCreateMatrix.forward_obj).asShort()
            up = data.inputValue(TateCreateMatrix.up_obj).asShort()
            # print "axis", axis
            # print "forward", forward
            # print "up", up, "\n"
            vector1 = (forward_point - base_point).normalize()
            vector2 = (up_point - base_point).normalize()

            crossProduct1 = (vector1 ^ vector2) * -1
            if crossProduct1 == om.MVector(0, 0, 0):
                data.setClean(plug)
                return
            crossProduct2 = vector1 ^ crossProduct1
            
            if axis == 0:
                if forward == 1:
                    x = vector1*-1
                else:
                    x = vector1
                if up == 1:
                    y = crossProduct2*-1
                else:
                    y = crossProduct2
                z = crossProduct1
                t = base_point
            elif axis == 1:
                if forward == 1:
                    x = vector1*-1
                    crossProduct1 *= -1
                else:
                    x = vector1
                if up == 1:
                    y = crossProduct1*-1
                else:
                    y = crossProduct1
                z = crossProduct2
                t = base_point
            elif axis == 2:
                if forward == 1:
                    y = vector1*-1
                else:
                    y = vector1
                if up == 1:
                    x = crossProduct2*-1
                else:
                    x = crossProduct2
                z = crossProduct1
                t = base_point
            elif axis == 3:
                crossProduct1 *= -1
                if forward == 1:
                    y = vector1*-1
                    crossProduct1 *= -1
                else:
                    y = vector1
                if up == 1:
                    x = crossProduct1*-1
                else:
                    x = crossProduct1
                z = crossProduct2
                t = base_point
            elif axis == 4:
                if forward == 1:
                    y = crossProduct1
                else:
                    y = crossProduct1*-1
                if up == 1:
                    y = crossProduct1
                    x = crossProduct2*-1
                else:
                    x = crossProduct2
                if (forward == 1) & (up == 1):
                    x = crossProduct2*-1
                    y = crossProduct1*-1
                z = vector1
                t = base_point
            elif axis == 5:
                if forward == 1:
                    x = crossProduct1*-1
                else:
                    x = crossProduct1
                if up == 1:
                    x = crossProduct1*-1
                    y = crossProduct2*-1
                else:
                    y = crossProduct2
                if (forward == 1) & (up == 1):
                    x = crossProduct1
                    y = crossProduct2*-1
                z = vector1*-1
                t = base_point

            matrix = om.MMatrix()
            matrix.setElement(0, 0, x[0])
            matrix.setElement(0, 1, x[1])
            matrix.setElement(0, 2, x[2])
            matrix.setElement(0, 3, 0)
            
            matrix.setElement(1, 0, y[0])
            matrix.setElement(1, 1, y[1])
            matrix.setElement(1, 2, y[2])
            matrix.setElement(1, 3, 0)
            
            matrix.setElement(2, 0, z[0])
            matrix.setElement(2, 1, z[1])
            matrix.setElement(2, 2, z[2])
            matrix.setElement(2, 3, 0)
            
            matrix.setElement(3, 0, t[0])
            matrix.setElement(3, 1, t[1])   
            matrix.setElement(3, 2, t[2])
            matrix.setElement(3, 3, 1)

            outputParentInverseM = data.inputValue(TateCreateMatrix.outputParentInverseMatrix_obj).asFloatMatrix()
            finalMatrix = matrix * om.MMatrix(outputParentInverseM)

            translate = om.MTransformationMatrix(finalMatrix).translation(om.MSpace.kWorld)
            rotate = om.MTransformationMatrix(finalMatrix).rotation(asQuaternion=False)

            outputT = data.outputValue(TateCreateMatrix.outputTranslate_obj)
            outputR = data.outputValue(TateCreateMatrix.outputRotate_obj)
            outputT.set3Double(*translate)
            outputR.set3Double(*rotate)

            data.setClean(plug)
            
    @classmethod
    def creator(cls):
        return TateCreateMatrix()
    
    @classmethod
    def initialize(cls):
        matrix_attr = om.MFnMatrixAttribute()
        enum_attr = om.MFnEnumAttribute()
        numeric_attr = om.MFnNumericAttribute()
        unit_attr = om.MFnUnitAttribute()

        cls.baseMatrix_obj = matrix_attr.create("baseMatrix", "baseMatrix", om.MFnMatrixData.kMatrix)
        matrix_attr.keyable = True
        matrix_attr.readable = False

        cls.vector1Matrix_obj = matrix_attr.create("vector1Matrix", "vec1", om.MFnMatrixData.kMatrix)
        matrix_attr.keyable = True
        matrix_attr.readable = False

        cls.vector2Matrix_obj = matrix_attr.create("vector2Matrix", "vec2", om.MFnMatrixData.kMatrix)
        matrix_attr.keyable = True
        matrix_attr.readable = False
    
        cls.axis_obj = enum_attr.create("axis", "ax", 0)
        enum_attr.addField("xyz", 0)
        enum_attr.addField("xzy", 1)
        enum_attr.addField("yxz", 2)
        enum_attr.addField("yzx", 3)
        enum_attr.addField("zxy", 4)
        enum_attr.addField("zyx", 5)
        enum_attr.keyable = True
        enum_attr.readable = True

        cls.forward_obj = enum_attr.create("forward", "fo", 0)
        enum_attr.addField("0", 0)
        enum_attr.addField("1", 1)
        enum_attr.keyable = True
        enum_attr.readable = True

        cls.up_obj = enum_attr.create("up", "up1", 0)
        enum_attr.addField("0", 0)
        enum_attr.addField("1", 1)
        enum_attr.keyable = True
        enum_attr.readable = True

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

        cls.outputRX_obj = unit_attr.create("rotateX", "rx", om.MFnUnitAttribute.kAngle, 0.0)
        unit_attr.keyable = True
        unit_attr.readable = False
        cls.outputRY_obj = unit_attr.create("rotateY", "ry", om.MFnUnitAttribute.kAngle, 0.0)
        unit_attr.keyable = True
        unit_attr.readable = False
        cls.outputRZ_obj = unit_attr.create("rotateZ", "rz", om.MFnUnitAttribute.kAngle, 0.0)
        unit_attr.keyable = True
        unit_attr.readable = False
        cls.outputRotate_obj = numeric_attr.create("outputRotate", "outputRotate",
                                                    cls.outputRX_obj, cls.outputRY_obj, cls.outputRZ_obj)
        numeric_attr.writable = False

        cls.addAttribute(cls.baseMatrix_obj)
        cls.addAttribute(cls.vector1Matrix_obj)
        cls.addAttribute(cls.vector2Matrix_obj)
        cls.addAttribute(cls.axis_obj)
        cls.addAttribute(cls.forward_obj)
        cls.addAttribute(cls.up_obj)
        cls.addAttribute(cls.outputParentInverseMatrix_obj)
        cls.addAttribute(cls.outputTranslate_obj)
        cls.addAttribute(cls.outputRotate_obj)

        cls.attributeAffects(cls.baseMatrix_obj, cls.outputTranslate_obj)
        cls.attributeAffects(cls.vector1Matrix_obj, cls.outputTranslate_obj)
        cls.attributeAffects(cls.vector2Matrix_obj, cls.outputTranslate_obj)
        cls.attributeAffects(cls.axis_obj, cls.outputTranslate_obj)
        cls.attributeAffects(cls.forward_obj, cls.outputTranslate_obj)
        cls.attributeAffects(cls.up_obj, cls.outputTranslate_obj)
        cls.attributeAffects(cls.outputParentInverseMatrix_obj, cls.outputTranslate_obj)

        cls.attributeAffects(cls.baseMatrix_obj, cls.outputRotate_obj)
        cls.attributeAffects(cls.vector1Matrix_obj, cls.outputRotate_obj)
        cls.attributeAffects(cls.vector2Matrix_obj, cls.outputRotate_obj)
        cls.attributeAffects(cls.axis_obj, cls.outputRotate_obj)
        cls.attributeAffects(cls.forward_obj, cls.outputRotate_obj)
        cls.attributeAffects(cls.up_obj, cls.outputRotate_obj)
        cls.attributeAffects(cls.outputParentInverseMatrix_obj, cls.outputRotate_obj)

def initializePlugin(plugin):

    vendor = "cho wooseoung"
    version = "1.0.0"

    pluginFn = om.MFnPlugin(plugin, vendor, version)

    try:
        pluginFn.registerNode(TateCreateMatrix.TYPE_NAME,
                                TateCreateMatrix.TYPE_ID,
                                TateCreateMatrix.creator,
                                TateCreateMatrix.initialize,
                                om.MPxNode.kDependNode)
    except:
        om.MGlobal.displayError("Failed to register node : {0}".format(TateCreateMatrix.TYPE_NAME))

def uninitializePlugin(plugin):
    
    pluginFn = om.MFnPlugin(plugin)

    try:
        pluginFn.deregisterNode(TateCreateMatrix.TYPE_ID)
    except:
        om.MGlobal.displayError("Failed to deregister node : {0}".format(TateCreateMatrix.TYPE_NAME))


if __name__ == "__main__":
    
    mc.file(new=True, force=True)
    plugin_name = "tate_createMatrix.py"

    mc.evalDeferred("if mc.pluginInfo('{0}', q=True, loaded=True): mc.unloadPlugin('{0}')".format(plugin_name))
    mc.evalDeferred("if not mc.pluginInfo('{0}', q=True, loaded=True): mc.loadPlugin('{0}')".format(plugin_name))
    
    mc.evalDeferred("m = mc.createNode('tate_createMatrix')")
    
    mc.evalDeferred("q = mc.sphere(n='test_fit_POS', p=(0,0,0), ch=0)[0]")
    mc.evalDeferred("a = mc.spaceLocator(n='test_base', p=(0,0,0))[0]")
    mc.evalDeferred("b = mc.spaceLocator(n='test_up', p=(0,0,0))[0]")
    mc.evalDeferred("c = mc.spaceLocator(n='test_follow', p=(0,0,0))[0]")
    mc.evalDeferred("mc.parent([a,b,c], q)")

    mc.evalDeferred("mc.setAttr('{0}.tx'.format(c), 1)")
    mc.evalDeferred("mc.setAttr('{0}.ty'.format(b), 1)")

    mc.evalDeferred("mc.addAttr('{0}'.format(q), ln='axis', at='enum', en='xyz:xzy:yxz:yzx:zxy:zyx', dv=0, k=1)")
    mc.evalDeferred("mc.addAttr('{0}'.format(q), ln='forward', at='enum', en='0:1', dv=0, k=1)")
    mc.evalDeferred("mc.addAttr('{0}'.format(q), ln='up', at='enum', en='0:1', dv=0, k=1)")
    
    mc.evalDeferred("mc.connectAttr('{0}.axis'.format(q), '{0}.axis'.format(m))")
    mc.evalDeferred("mc.connectAttr('{0}.forward'.format(q), '{0}.forward'.format(m))")
    mc.evalDeferred("mc.connectAttr('{0}.up'.format(q), '{0}.up'.format(m))")

    mc.evalDeferred("mc.connectAttr('{0}.worldMatrix[0]'.format(a), '{0}.baseMatrix'.format(m))")
    mc.evalDeferred("mc.connectAttr('{0}.worldMatrix[0]'.format(c), '{0}.vector1Matrix'.format(m))")
    mc.evalDeferred("mc.connectAttr('{0}.worldMatrix[0]'.format(b), '{0}.vector2Matrix'.format(m))")
    
    mc.evalDeferred("output = mc.group(n='output', em=True)")
    mc.evalDeferred("mc.connectAttr('{0}.parentInverseMatrix[0]'.format(output), '{0}.outputParentInverseMatrix'.format(m))")
    mc.evalDeferred("mc.connectAttr('{0}.outputTranslate'.format(m), '{0}.t'.format(output))")
    mc.evalDeferred("mc.connectAttr('{0}.outputRotate'.format(m), '{0}.r'.format(output))")
    mc.evalDeferred("mc.setAttr('output.displayLocalAxis', 1)")
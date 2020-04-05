import pymel.core as pm
import copy


def edit_enum():
    pass

def edit_int():
    pass

def edit_vector():
    pass

def edit_string():
    pass

def edit_float():
    pass

def edit_bool():
    pass

class AttrControl(object):

    def __init__(self):
        self.reset_attr_attr()
        
    def add_attr(self, sel):
        kwargs = copy.deepcopy(vars(a))
        for i in vars(a):
            if kwargs[i] == None:
                del kwargs[i]
            elif i == "longName":
                ln = kwargs[i]
                del kwargs[i]
            elif i == "lock":
                lock = kwargs[i]
                del kwargs[i]

        for i in sel:
            i.addAttr(ln, **kwargs)
            i.setAttr(ln, lock=lock)
            if self.type == "string":
                i.setAttr(ln, self.string)
        
    def edit_attr(self):
        pass
    
    def get_attr_list(self, node):
        if isinstance(node, pm.nodetypes.Transform):
            dfAttr = [node.attr("tx"), node.attr("tx"), node.attr("tx")
                    , node.attr("rx"), node.attr("rx"), node.attr("rx")
                    , node.attr("sx"), node.attr("sx"), node.attr("sx")
                    , node.attr("v")]
        else:
            dfAttr = []
        kaAttr = []
        udAttr = []
        childList = []

        for i in node.listAttr(keyable=True, userDefined=True):
            if not i.isChild():
                kaAttr.append(i)
            else:
                childList.append(i)
        
        parAttr = []
        for i in node.listAttr(userDefined=True):
            if i.getParent():
                check = []
                for x in i.getParent().getChildren():
                    if not x.isKeyable():
                        check.append(False)
                    else:
                        check.append(True)
                if True not in check:
                    if i.getParent() in kaAttr:
                        kaAttr.remove(i.getParent())
                    udAttr.append(i.getParent())
                elif False not in check:
                    if i.getParent() in udAttr:
                        udAttr.remove(i.getParent())
                else: 
                    udAttr.append(i.getParent())
            elif not i.isKeyable():
                udAttr.append(i)
        udAttr = list(set(udAttr))
        return dfAttr, kaAttr, udAttr
    
    def get_attr_attr(self, attr):
        self.longName = attr.longName()
        self.shortName = attr.shortName()
        self.type = attr.type()
        self.keyable = attr.isKeyable()
        self.minValue = attr.getMin()
        self.maxvalue = attr.getMax()
        self.lock = attr.isLocked()
        self.dv = attr.getDefault()
        if self.type == "enum":
            self.enumDict = attr.getEnums()
        if self.type == "string":
            self.string = attr.get()

    def set_attr_attr(self, **args):
        for i in vars(self).keys():
            if i in args.keys():
                if type(args[i]) == str:
                    exec("self.{0} = '{1}'".format(i, args[i]))
                else:
                    exec("self.{0} = {1}".format(i, args[i]))

    def reset_attr_attr(self):
        self.longName = None
        self.shortName = None
        self.type = None
        self.hxv = None
        self.hnv = None
        self.minValue = None
        self.maxvalue = None
        self.enumDict = None
        self.keyable = None
        self.lock = None
        self.string = None
        self.dv = None

    def print_attr_attr(self):
        strFormat = '%-10s%-10s%-10s'
        print "------------------ attr_attr ------------------"
        print strFormat % ("ln : "    , self.longName , type(self.longName))
        print strFormat % ("sn : "    , self.shortName, type(self.shortName))
        print strFormat % ("type : "  , self.type     , type(self.type))
        print strFormat % ("hxv : "   , self.hxv      , type(self.hxv))
        print strFormat % ("hnv : "   , self.hnv      , type(self.hnv))
        print strFormat % ("min : "   , self.minValue , type(self.minValue))
        print strFormat % ("max : "   , self.maxvalue , type(self.maxvalue))
        print strFormat % ("en : "    , self.enumDict , type(self.enumDict))
        print strFormat % ("key : "   , self.keyable  , type(self.keyable))
        print strFormat % ("lock : "  , self.lock     , type(self.lock))
        print strFormat % ("string : ", self.string   , type(self.string))
        print strFormat % ("dv : "    , self.dv       , type(self.dv))
        print "-----------------------------------------------"

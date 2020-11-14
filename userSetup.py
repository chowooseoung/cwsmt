# -*- coding:utf-8 -*-

import maya.api.OpenMaya as om
import pymel.core as pm
import maya.cmds as mc
import maya.mel as mel
import pprint
import os
import sys

inhouse_shelf = "inhouse"

def create_inhouse_shelf():
    
    shelf_layout = pm.mel.globals["gShelfTopLevel"]
    last_selected_tab = pm.tabLayout(shelf_layout, query=True, selectTab=True)

    # remove inhouse shelf
    tabs = pm.tabLayout(shelf_layout, query=True, childArray=True)
    if inhouse_shelf in tabs:
        pm.deleteUI(inhouse_shelf)

    # add inhouse shelf
    inhouse = pm.shelfLayout(inhouse_shelf, parent=shelf_layout)
    tabs = pm.tabLayout(shelf_layout, query=True, childArray=True)
    inhouse_index = tabs.index(inhouse.shortName()) + 1
    custom_index = tabs.index("Custom") + 1
    pm.tabLayout(shelf_layout, edit=True, moveTab=(inhouse_index, custom_index+1))

    # re select last tab
    tabs = pm.tabLayout(shelf_layout, query=True, childArray=True)
    index = tabs.index(last_selected_tab) + 1
    pm.tabLayout(shelf_layout, edit=True, selectTabIndex=index)

    # scripts interface shelfbutton add inhouse shelf
    pm.shelfButton(
        parent=inhouse,  
        image=r"D:\maya\scripts\scriptsinterface\scriptsinterface.png",
        command='''from scriptsinterface import mayaui;mayaui.SiMaya.display("guest")''', 
        label="ScriptsInterface",
        sourceType="python",
        annotation="inhouse scripts interface tool"
    )

pm.evalDeferred(create_inhouse_shelf, low=True)
pm.mel.eval('''commandPort -name "localhost:7001" -sourceType "mel" -echoOutput;''')
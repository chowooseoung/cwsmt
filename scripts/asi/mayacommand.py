# -*- coding:utf-8 -*-

import pymel.core as pm


def add_shelf_button():
    current_tab = pm.tabLayout("ShelfLayout", query=True, selectTab=True)

    pm.shelfButton(parent=,
                    image=,
                    command=,
                    doubleClickCommand=,
                    label=,
                    imageOverlayLabel=,
                    sourceType=,
                    annotation=)
# SPDX-FileCopyrightText: 2023 Brad Barnett
#
# SPDX-License-Identifier: MIT

import lvgl as lv
import gc
from . import _BasePanel, RoundMenuPanel, ZRoundMenuPanel, IndevManager, add_styles_to_children
from .menu_panels import add_back_menu_item
from tools.custom_views import FlexFlowView
from tools.focus_callbacks import pan_focus_cb


class CircularLivePanel(RoundMenuPanel):
    auto_add_back_btn = False
    animation = None
    zoomed = True
    style_key = 0
    auto_add_children = False

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def add_item(self, title, icon, func, params, callback, parent=None):
        if parent == None:
            parent = self.obj
        if func == ZRoundMenuPanel or func == CircularLivePanel:
            print(f"Cannot place a {func} on a ZoomedLivePanel.  Changing to RoundMenuPanel.")
            func = RoundMenuPanel
        panel = func(
            params=params,
            callback=callback,
            title=title,
            icon=icon,
            parent=parent,
            group=self.group,
            animation=None,
            size=self.obj.child_size,
            alignment=self.obj.get_next_child_align(),
            root=True,
        )
        self.subpanels.append(panel)
        panel.idm = self.idm
        return panel


class HorizontalLivePanel(_BasePanel):
    auto_add_back_btn = False
    auto_add_title = False
    flex_flow = lv.FLEX_FLOW.ROW
    auto_add_children = False

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.menu_def = self.params.copy()
        add_back_menu_item(self)

        self.obj_size = (lv.pct(100), lv.pct(100))
        self.update_layout()

        self.obj = obj = FlexFlowView(self, self.flex_flow)

        for item in self.menu_def:
            self.add_item(*item)

        self.group.set_focus_cb(lambda g: pan_focus_cb(g, self.obj))

        self.finalize()

    def add_item(self, title, icon, func, params, callback, parent=None):
        if parent == None: parent = self.obj
        if func == ZRoundMenuPanel or func == CircularLivePanel:
            print(f"Cannot place a {func} on a FlexFlowLivePanel.  Changing to RoundMenuPanel.")
            func = RoundMenuPanel
        panel = func(
            params=params,
            title=title,
            icon=icon,
            parent=parent,
            callback=callback,
            group=self.group,
            animation=None,
            size=(lv.pct(100), lv.pct(100)),
            alignment=(lv.ALIGN.CENTER, 0, 0),
            root=True,
        )
        panel.idm = self.idm
        self.subpanels.append(panel)
        return panel


class VerticalLivePanel(HorizontalLivePanel):
    flex_flow = lv.FLEX_FLOW.COLUMN


class TabViewLivePanel(_BasePanel):
    auto_add_title = False
    auto_add_back_btn = False
    style_key = 0

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.menu_def = self.params.copy()
        add_back_menu_item(self)

        self.obj_size = (lv.pct(100), lv.pct(100))
        self.update_layout()

        menu_width = max(self.get_width() - self.get_height(), 80)
        self.obj = obj = lv.tabview(self, lv.DIR.LEFT, menu_width)

        tab_btns = obj.get_tab_btns()  # The BtnMatrix containing the buttons
        add_styles_to_children(tab_btns, include_self=True)
        tab_btns.add_event(
            lambda e: self.subpanels[e.get_target_obj().get_selected_btn()].idm.peek(),
            lv.EVENT.VALUE_CHANGED,
            None,
        )
        self.group.add_obj(tab_btns)
        self.group.set_editing(True)

        tabs = [None] * len(self.menu_def)
        for i, item in enumerate(self.menu_def):
            tabs[i] = obj.add_tab(item[0])
            self.add_item(*item, parent=tabs[i])
            tabs[i].set_style_pad_all(0, 0)
            self.subpanels[i].set_style_radius(0, 0)

        self.finalize()

        self.subpanels[0].idm.peek()

    def add_item(self, title, icon, func, params, callback, parent=None):
        if parent == None:
            parent = self.obj
        panel = func(
            params=params,
            callback=callback,
            title=None,
            icon=icon,
            parent=parent,
            idm=IndevManager(self.idm.indevs),
            animation=None,
            size=(lv.pct(100), lv.pct(100)),
            alignment=(lv.ALIGN.CENTER, 0, 0),
            obj_size=(lv.pct(95), lv.pct(95)),
            root=True,
        )
        self.subpanels.append(panel)
        return panel

# create_panel isn't used yet.  Will try to use it with all live panels in the future
def create_panel(self, title, icon, func, params, callback, parent, alignment=(lv.ALIGN.CENTER, 0, 0), 
                 no_title=False, obj_size=None, size=(lv.pct(100), lv.pct(100))):
    title = title if not no_title else None
    if self.auto_add_children:
        group = None
        idm = IndevManager(self.idm.indevs)
    else:
        group = self.group
        idm = None
    return func(
        title=title,
        icon=icon,
        params=params,
        callback=callback,
        parent=parent,
        alignment=alignment,
        obj_size=obj_size,
        size=size,
        idm=idm,
        animation=None,
        root=True,
        group=group,
    )

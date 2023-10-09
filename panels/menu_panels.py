# SPDX-FileCopyrightText: 2023 Brad Barnett
#
# SPDX-License-Identifier: MIT

import lvgl as lv
from . import _BasePanel, BtnMatrixPanel, BtnPanel, ListPanel
from tools.custom_views import RoundView
from tools.focus_callbacks import rotate_focus_cb, pan_focus_cb


class MatrixMenuPanel(BtnMatrixPanel):
    zoomed = False
    def __init__(self, *args, params, callback=None, **kwargs):
        menu_def = params.copy()
        menu_length = len(menu_def)

        rows = columns = 1
        while rows * columns < menu_length:
            rows += 1
            if rows * columns < menu_length:
                columns += 1

        btn_map = []
        ctrl_map = [1] * menu_length
        cb_map = []
        one_checked = True
        for r in range(rows):
            for c in range(columns):
                i = r * columns + c
                if i >= menu_length:
                    break
                btn_map.append(menu_def[i][0])
                cb_map.append(create_cb(self, *menu_def[i]))
            btn_map.append("\n")
        btn_map.append("")

        bm_params = (btn_map, ctrl_map, one_checked)
        
        super().__init__(*args, params=bm_params, callback = cb_map, **kwargs)

class ListMenuPanel(ListPanel):
    zoomed = False
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def add_item(self, title, icon, func, params, callback):
        btn = self.obj.add_btn(icon, title)
        btn.add_event(create_cb(self, title, icon, func, params, callback, btn), lv.EVENT.SHORT_CLICKED, None)
        self.group.add_obj(btn)

class RoundMenuPanel(_BasePanel):
    close_align = (lv.ALIGN.CENTER, 0, 0)
    title_align = (lv.ALIGN.TOP_LEFT, 0, 0)
    zoomed = False

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.root: self.title_align = (lv.ALIGN.CENTER, 0, 0)

        self.menu_def = self.params.copy()
        if self.zoomed: add_close_menu_item(self)

        self.obj_size = None
        self.obj = RoundView(self, len(self.menu_def), self.zoomed)

        for item in self.menu_def:
            self.add_item(*item)

        if self.rotate:
            self.group.set_focus_cb(lambda g: rotate_focus_cb(g, self.obj, exclude=[self.close_btn]))
        elif self.zoomed:
            self.group.set_focus_cb(lambda g: pan_focus_cb(g, self.obj, scroll_gp=True))

        self.post_config()

    def add_item(self, title, icon, func, params, callback):
        btn = self.obj.add_btn(icon, title)
        btn.add_event(create_cb(self, title, icon, func, params, callback, btn), lv.EVENT.SHORT_CLICKED, None)
        self.group.add_obj(btn)

class ZRoundMenuPanel(RoundMenuPanel):
    style_key = 0
    auto_add_close_btn = False
    auto_add_title = False
    animation = None
    zoomed = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def add_item(self, title, icon, func, params, callback):
        btn = self.obj.add_btn(icon, title)
        btn.add_event(create_cb(self, title, icon, func, params, callback, btn, self.obj.child_size),
                       lv.EVENT.SHORT_CLICKED, None)
        self.group.add_obj(btn)


###############################################################################################

def add_close_menu_item(self):
    if not self.root:
        if type(self) == ZRoundMenuPanel:
            self.menu_def.insert(0, (self.close_btn_label, self.close_btn_icon, self.close, None, None))
        else:
            self.menu_def.insert(0, (self.close_btn_label, self.close_btn_icon, BtnPanel, None, self.close))

def create_cb(self, title, icon, func, params, callback, sender=None, size=None):
    if func == None: func = self.callback
    
    return lambda e: func(
        e,
        title=title,
        icon=icon,
        params=params,
        callback=callback,
        sender=sender if sender else self,
        parent=self,
        idm=self.idm,
        size=size if size else self.size,
        alignment=determine_pos(e, self)
    )

def determine_pos(e, parent):
    if parent.zoomed:
        return (lv.ALIGN.TOP_LEFT, e.get_target_obj().get_x(), e.get_target_obj().get_y())
    else:
        return (lv.ALIGN.CENTER, 0, 0)

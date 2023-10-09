# SPDX-FileCopyrightText: 2023 Brad Barnett
#
# SPDX-License-Identifier: MIT

import lvgl as lv
import gc
from . import config, apply_styles, IndevManager, add_children_to_group
from tools.misc import add_btn, add_label, make_square


class _BasePanel(lv.obj):
    style_key = None

    auto_add_close_btn = True
    auto_add_title = True
    auto_add_children = True
    auto_add_styles = True
    close_align = (lv.ALIGN.BOTTOM_MID, 0, lv.pct(-1))
    title_align = (lv.ALIGN.TOP_MID, 0, lv.pct(3))
    obj_size = config.default_obj_size
    close_btn_icon = config.close_btn_icon
    close_btn_label = config.close_btn_label
    close_btn_size = (lv.pct(15), lv.pct(15))
    warn = config.warn
    
    def __init__(
        self,
        event=None,
        *,
        parent,
        params=None,
        callback=None,
        rotate=None,
        idm=None,
        title=None,
        root=False,
        sender=None,
        obj_size=None,
        group=None,
        animation = -1,
        icon=config.default_icon,
        size=(lv.pct(100), lv.pct(100)),
        alignment=(lv.ALIGN.CENTER, 0, 0),
    ):
        super().__init__(parent)
        if self.style_key is None: self.style_key = config.panel_style_key
        self.callback = config.default_callback if callback is None else callback
        self.rotate = config.rotate if rotate is None else rotate
        self.animation = config.animation if animation == -1 else animation
        self.group = group if group else lv.group_create()
        if obj_size: self.obj_size = obj_size  # Size to set self.obj in .post_config()
        self.params = params  # paremeters for the obj
        self.parent = parent  #
        self.idm = idm  #
        self.size = size  #
        self.icon = icon  #
        self.title = title  #
        self.event = event  #
        self.root = root  # Root panels don't get a close button
        self.sender = sender  # Animations may get position information from this

        self.obj = None  # The object created by the Subclass
        self.timers = [] # Timers created by subclasses, such as the refresh timer in LabelPanel
        self.title_label = None # Must point to something for exclusions in subclass animations
        self.close_btn = None  #   like MenuPanel rotate
        self.animations = []  # List of animations created by subclasses like AnalogClockPanel
        self.subpanels = []  # List of subpanels created by LivePanels

        apply_styles(self)
        self.align(*alignment)
        self.set_size(*self.size)
        self.clear_flag(lv.obj.FLAG.SCROLLABLE)
        # self.parent.clear_flag(lv.obj.FLAG.SCROLLABLE)

    def post_config(self):
        if self.idm: self.idm.push(self.group)

        if self.auto_add_close_btn and not self.root:
            self.close_btn = add_btn(self, self.close_btn_icon, "", self.close_btn_size, self.close_align, self.close)
            self.close_btn.add_flag(lv.obj.FLAG.FLOATING)
            make_square(self.close_btn)
            self.close_btn.move_foreground()

        if self.auto_add_title and self.title:  
            self.title_label = add_label(self, self.title, self.title_align)
            self.title_label.add_flag(lv.obj.FLAG.FLOATING)
            self.title_label.move_foreground()

        if self.auto_add_styles: apply_styles(self)

        if self.obj and self.obj_size:
            self.obj.set_size(*self.obj_size)
            self.obj.center()

        if self.auto_add_children: add_children_to_group(self, self.group)

        if self.close_btn: lv.group_focus_obj(self.close_btn)

        if self.animation:
            self.update_layout()

            dest_area = lv.area_t()
            self.get_coords(dest_area)
            dest_area.x1 = self.get_x()
            dest_area.y1 = self.get_y()

            start_area = lv.area_t()
            if self.sender: self.sender.get_coords(start_area)

            self.animation(self, start_area, dest_area, shrink=False)

        gc.collect()

    def close(self, event=None, **kwargs):

        if self.animation:
            self.update_layout()

            start_area = lv.area_t()
            self.get_coords(start_area)

            dest_area = lv.area_t()
            if self.sender: self.sender.get_coords(start_area)

            self.animation(self, start_area, dest_area, shrink=True, del_obj=True)
            self.cleanup()
        else:
            self.cleanup()
            self.delete()

    def cleanup(self):
        if self.idm:
            self.idm.pop()
            self.group.set_focus_cb(None)

        for panel in self.subpanels:
            panel.cleanup()
            panel.delete()
        for timer in self.timers:
            timer.set_repeat_count(0)
        for anim in self.animations:
            anim.custom_del(None)
        gc.collect()


class CustomPanel(_BasePanel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        func = self.params if callable(self.params) else None

        self.obj = obj = lv.obj(self)
        obj.add_flag(lv.obj.FLAG.SCROLL_ON_FOCUS)

        if func:
            gridnav = func(obj)
        else:
            gridnav = True

        if gridnav:
            lv.gridnav_add(obj, lv.GRIDNAV_CTRL.ROLLOVER)
            obj.add_flag(lv.obj.FLAG.CLICK_FOCUSABLE)
        else:
            obj.clear_flag(lv.obj.FLAG.CLICKABLE)
            add_children_to_group(obj, self.group)

        self.post_config()

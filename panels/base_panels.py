# SPDX-FileCopyrightText: 2023 Brad Barnett
#
# SPDX-License-Identifier: MIT

import lvgl as lv
import gc
from . import config, add_styles_to_children, IndevManager, add_children_to_group
from tools.misc import add_btn, add_label, make_square


class _BasePanel(lv.obj):
    style_key = None

    auto_add_back_btn = True
    auto_add_title = True
    auto_add_children = True
    back_align = (lv.ALIGN.BOTTOM_MID, 0, lv.pct(-3))
    title_align = (lv.ALIGN.TOP_MID, 0, lv.pct(3))
    obj_size = (lv.pct(66), lv.pct(66))
    
    def __init__(
        self,
        event=None,
        *,
        params=None,
        callback=None,
        rotate=None,
        parent,
        idm=None,
        size=(lv.pct(100), lv.pct(100)),
        icon=lv.SYMBOL.HOME,
        title=None,
        root=False,
        sender=None,
        obj_size=None,
        group=None,
        animation = -1,
        alignment=(lv.ALIGN.CENTER, 0, 0),
    ):
        super().__init__(parent)
        if self.style_key is None: self.style_key = config.panel_style_key
        self.callback = config.default_callback if callback is None else callback  # self.callback is used by the widgets in subclasses
        self.rotate = config.rotate if rotate is None else rotate
        self.animation = config.animation if animation == -1 else animation
        self.group = group if group else lv.group_create()
        if obj_size: self.obj_size = obj_size  # Size to set self.obj in .finalize()
        self.params = params  # paremeters for the obj
        self.parent = parent  #
        self.idm = idm  #
        self.size = size  #
        self.icon = icon  #
        self.title = title  #
        self.event = event  #
        self.root = root  # Root panels don't get a back button
        self.sender = sender  # Animations may get position information from the sender

        self.obj = None  # The object created by the Subclass
        self.timers = [] # Timers created by subclasses, such as the refresh timer in LabelPanel
        self.title_label = None # Must point to something for exclusions in subclass animations
        self.back_btn = None  #   like MenuPanel rotate
        self.animations = []  # List of animations created by subclasses like AnalogClockPanel
        self.subpanels = []  # List of subpanels created by LivePanels

        add_styles_to_children(self)
        self.align(*alignment)
        self.set_size(*self.size)
        self.clear_flag(lv.obj.FLAG.SCROLLABLE)
        self.parent.clear_flag(lv.obj.FLAG.SCROLLABLE)

    def finalize(self):
        if self.idm: self.idm.push(self.group)

        if self.auto_add_back_btn and not self.root:
            self.back_btn = add_btn(self, lv.SYMBOL.LEFT, "", (lv.pct(12), lv.pct(12)), self.back_align, self.go_back)
            self.back_btn.add_flag(lv.obj.FLAG.FLOATING)
            make_square(self.back_btn)
            self.back_btn.move_foreground()

        if self.auto_add_title and self.title:  
            self.title_label = add_label(self, self.title, self.title_align)
            self.title_label.add_flag(lv.obj.FLAG.FLOATING)
            self.title_label.move_foreground()

        add_styles_to_children(self)

        if self.obj and self.obj_size:
            self.obj.set_size(*self.obj_size)
            self.obj.center()

        if self.auto_add_children: add_children_to_group(self, self.group)

        if self.back_btn: lv.group_focus_obj(self.back_btn)

        if self.animation:
            self.update_layout()
            dest_params = (
                self.get_x(),
                self.get_y(),
                self.get_width(),
                self.get_height(),
            )
            if self.sender:
                start_params = (
                    self.sender.get_x_aligned(),
                    self.sender.get_y_aligned(),
                    self.sender.get_width(),
                    self.sender.get_height(),
                )
            else:
                start_params = 0, 0, 0, 0
            self.animation(self, start_params, dest_params)

        gc.collect()

    def go_back(self, event=None, **kwargs):
        if self.idm: self.idm.pop()

        if self.animation:
            self.update_layout()
            start_params = (
                self.get_x(),
                self.get_y(),
                self.get_width(),
                self.get_height(),
            )
            if self.sender:
                dest_params = (
                    self.sender.get_x_aligned(),
                    self.sender.get_y_aligned(),
                    self.sender.get_width(),
                    self.sender.get_height(),
                )
            else:
                dest_params = 0, 0, 0, 0
            self.animation(self, start_params, dest_params, del_obj=True)
            self._del()
        else:
            self._del()
            self.delete()

    def _del(self):
        self.group.set_focus_cb(None)
        for timer in self.timers:
            timer.set_repeat_count(0)
        for anim in self.animations:
            anim.custom_del(None)
        for panel in self.subpanels:
            panel._del()
            panel.delete()
        gc.collect()


class _ExamplePanel(_BasePanel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        param1, param2, param3 = self.params
        self.obj = obj = lv.obj(self)

        obj.add_event(self.callback, lv.EVENT.ALL, None)

        self.finalize()


class CustomPanel(_BasePanel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        cmd = self.params

        self.obj = obj = lv.obj(self)
        obj.add_flag(lv.obj.FLAG.SCROLL_ON_FOCUS)

        if cmd:
            gridnav = cmd(obj)
        else:
            gridnav = True

        if gridnav:
            lv.gridnav_add(obj, lv.GRIDNAV_CTRL.ROLLOVER)
            obj.add_flag(lv.obj.FLAG.CLICK_FOCUSABLE)
        else:
            obj.clear_flag(lv.obj.FLAG.CLICKABLE)
            add_children_to_group(obj, self.group)

        self.finalize()

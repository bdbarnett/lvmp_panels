# SPDX-FileCopyrightText: 2023 Brad Barnett
#
# SPDX-License-Identifier: MIT

import lvgl as lv
from panels import _BasePanel, CustomPanel
from panels import AnalogClockPanel, ArcPanel, BtnPanel, BtnMatrixPanel, CalendarPanel, \
    ColorWheelPanel, LabelPanel, ListPanel, RollerPanel, SliderPanel, TextAreaPanel
from panels import ListMenuPanel, MatrixMenuPanel, RoundMenuPanel, ZRoundMenuPanel
from panels import RoundMenuPanel as DefaultMenuPanel
from tools.repl import Lv_Repl
from tools.images import ImageCache
# from tools.events import debug_event_cb
import gc           # just for testing with a LabelPanel that runs gc.mem_free()

ic = ImageCache("images/")

list_items = [
    ("File"),
    ("New", lv.SYMBOL.FILE, lambda e, title: print(f"Pressed {title}")),
    ("Open", lv.SYMBOL.DIRECTORY, lambda e, title: print(f"Pressed index {e.get_target_obj().get_index()}")),
    ("Save", lv.SYMBOL.SAVE, None),
    ("Delete", lv.SYMBOL.CLOSE, None),
    ("Edit", lv.SYMBOL.EDIT, None),
    ("Connectivity"),
    ("Bluetooth", lv.SYMBOL.BLUETOOTH, None),
    ("Navigation", lv.SYMBOL.GPS, None),
    ("USB", lv.SYMBOL.USB, None),
    ("Battery", lv.SYMBOL.BATTERY_FULL, None),
    ("Exit"),
    ("Apply", lv.SYMBOL.OK, None),
    ("Close", lv.SYMBOL.CLOSE, None)
    ]

roller_items = [
    "Africa",
    "Antarctica",
    "Asia",
    "Australia",
    "Europe",
    "North America",
    "South America",
    ]

bm_btn_map = [
    "1", "2", "3", "4", "\n",
    "5", "6", "7", "8", "\n",
    "9", "10", "11", "12", "\n",
    "A", "B", "C", "D", ""
    ]
bm_ctrl_map = [1 | lv.btnmatrix.CTRL.CHECKABLE | lv.btnmatrix.CTRL.POPOVER]*16
bm_cb_map = [lambda e: print(f"Index {e.get_target_obj().get_selected_btn()} was selected.  Checked = { \
    e.get_target_obj().has_btn_ctrl(e.get_target_obj().get_selected_btn(), lv.btnmatrix.CTRL.CHECKED)}")]*16

def custom_checkboxes(parent):
    gridnav = False
    text_map = ["Apple", "Banana", "Lemon", "Melon"]
    state_map = [lv.STATE.DEFAULT, lv.STATE.CHECKED, lv.STATE.DISABLED, lv.STATE.CHECKED | lv.STATE.DISABLED]
    cb_map = [lambda e: print(f"Item {e.get_target_obj().get_text()} changed.  Checked = { \
                e.get_target_obj().has_state(lv.STATE.CHECKED)}")]*5
    parent.set_flex_flow(lv.FLEX_FLOW.COLUMN)
    parent.set_flex_align(lv.FLEX_ALIGN.CENTER, lv.FLEX_ALIGN.START, lv.FLEX_ALIGN.CENTER)

    for i in range(len(text_map)):
        checkbox = lv.checkbox(parent)
        checkbox.add_state(state_map[i])
        checkbox.set_text(text_map[i])
        checkbox.add_event(cb_map[i], lv.EVENT.VALUE_CHANGED, None)

    return gridnav

def custom_sliders(parent):
    gridnav = False
    label_map = ["A", "B", "C", "D", "E"]
    value_map = [25, 75, 50, 100, 50]
    cb_map = [lambda e: print(f"Item {e.get_target_obj()} changed.  Value = { \
                e.get_target_obj().get_value()}")]*5
    parent.set_flex_flow(lv.FLEX_FLOW.ROW)
#    parent.set_flex_align(lv.FLEX_ALIGN.CENTER, lv.FLEX_ALIGN.START, lv.FLEX_ALIGN.CENTER)

    for i in range(len(label_map)):
        slider = lv.slider(parent)
        slider.set_size(lv.pct(20), lv.pct(100))
        slider.set_range(0, 100)
        slider.set_value(value_map[i], lv.ANIM.ON)
        slider.add_event(cb_map[i], lv.EVENT.VALUE_CHANGED, None)
        label = lv.label(slider)
        label.set_text(label_map[i])
        label.center()

    return gridnav

def custom_switches(parent):
    gridnav = False
    label_map = ["One", "Two", "Three", "Four", "Five"]
    state_map = [lv.STATE.CHECKED, lv.STATE.DEFAULT, lv.STATE.CHECKED, lv.STATE.DISABLED, lv.STATE.CHECKED | lv.STATE.DISABLED]
    cb_map = [lambda e: print(f"Item {e.get_target_obj()} changed.  Checked = { \
                e.get_target_obj().has_state(lv.STATE.CHECKED)}")]*5
    parent.set_flex_flow(lv.FLEX_FLOW.COLUMN)
#    parent.set_flex_align(lv.FLEX_ALIGN.CENTER, lv.FLEX_ALIGN.START, lv.FLEX_ALIGN.CENTER)

    for i in range(len(label_map)):
        switch = lv.switch(parent)
        switch.set_size(lv.pct(100), lv.pct(20))
        switch.add_state(state_map[i])
        switch.add_event(cb_map[i], lv.EVENT.VALUE_CHANGED, None)
        label = lv.label(switch)
        label.set_text(label_map[i])
        label.center()

    return gridnav

volume_menu = [
    ("VolUp", lv.SYMBOL.PLUS, None, None, None),
    ("VolDwn", lv.SYMBOL.MINUS, None, None, None),
    ]

transport_menu = [
    ("Play", lv.SYMBOL.PLAY, lambda e, **args: print("Pressed Play"), None, None),
    ("Next", lv.SYMBOL.NEXT, lambda e, title, **args: print(f"Pressed {title}"), None, None),
    ("Volume", lv.SYMBOL.VOLUME_MAX, RoundMenuPanel, volume_menu, None),
    ("Mute", lv.SYMBOL.MUTE, None, None, None),
    ("Prev", lv.SYMBOL.PREV, None, None, None),
    ]

menu1 = [
    ("AClock", lv.SYMBOL.SETTINGS, AnalogClockPanel, None, None),
    ("Arc", lv.SYMBOL.SETTINGS, ArcPanel, (lambda: 50, (0, 100)),
        lambda e: print(f"Value: {e.get_target_obj().get_value()}")),
    ("BMatrix", lv.SYMBOL.SETTINGS, BtnMatrixPanel, (bm_btn_map, bm_ctrl_map, True), bm_cb_map),
    ("Button", lv.SYMBOL.SETTINGS, BtnPanel, None, None),
    ("Calendar", lv.SYMBOL.SETTINGS, CalendarPanel, None, None),
    ("ColorWheel", lv.SYMBOL.SETTINGS, ColorWheelPanel, lambda: lv.palette_main(lv.PALETTE.BLUE),
        lambda e: print(f"RGB set in: {e.get_target_obj().get_rgb()}")),
    ]

menu2 = [
    ("Label", lv.SYMBOL.SETTINGS, LabelPanel, ("Static Text", False), None),
    ("List", ic.img("icons8-list-16.png"), ListPanel, list_items, None),
    ("Roller", lv.SYMBOL.SETTINGS, RollerPanel, (lambda: 5, roller_items),
       lambda e: print(f"Selected: {e.get_target_obj().get_selected()}")),
    ("Slider", lv.SYMBOL.SETTINGS, SliderPanel, (lambda: 3, (1, 16)),
        lambda e: print(f"Value: {e.get_target_obj().get_value()}")),
    ("TextArea", lv.SYMBOL.SETTINGS, TextAreaPanel, "\n".join(roller_items), None),
    ]

menu3 = [
    ("Checks", lv.SYMBOL.SETTINGS, CustomPanel, custom_checkboxes, None),
    ("Sliders", lv.SYMBOL.SETTINGS, CustomPanel, custom_sliders, None),
    ("Switches", lv.SYMBOL.SETTINGS, CustomPanel, custom_switches, None),
    ("Mem_Free", lv.SYMBOL.SETTINGS, LabelPanel,
        (lambda: f"Free Memory: \n({gc.collect()}) {gc.mem_free():,}", 1000), None),
    ("REPL", lv.SYMBOL.SETTINGS, TextAreaPanel, Lv_Repl, None),
    ("Transport", lv.SYMBOL.AUDIO, DefaultMenuPanel, transport_menu, None),
    ]

main_menu = [
    ("LMenu 1", ic.img("icons8-list-16.png"), ListMenuPanel, menu1, None),
    ("MMenu 2", lv.SYMBOL.SETTINGS, MatrixMenuPanel, menu2, None),
    ("RMenu 3", lv.SYMBOL.SETTINGS, RoundMenuPanel, menu3, None),
    ("ZMenu 1", lv.SYMBOL.SETTINGS, ZRoundMenuPanel, menu1, None),
    ("LMenu 2", ic.img("icons8-list-16.png"), ListMenuPanel, menu2, None),
    ("MMenu 3", lv.SYMBOL.SETTINGS, MatrixMenuPanel, menu3, None),
    ]

live_panels =  main_menu + menu1 + menu2 + menu3

#!/opt/bin/lv_micropython -i

# SPDX-FileCopyrightText: 2023 Brad Barnett
#
# SPDX-License-Identifier: MIT

import display_driver
import lvgl as lv
from panels import RoundMenuPanel, ZoomedMenuPanel, ZoomedLivePanel, FlexFlowLivePanel
from encoders import EncoderWidget

from panels_demo_data import main_menu, live_panels

lv.disp_get_default().set_res(480, 640)

narrow_style = lv.style_t()
narrow_style.init()
narrow_style.set_pad_all(0)
narrow_style.set_margin_top(1)
narrow_style.set_margin_bottom(1)
narrow_style.set_margin_left(1)
narrow_style.set_margin_right(1)
narrow_style.set_border_width(0)

scr = lv.scr_act()
# scr.add_event( \
#     lambda e: print(f"Container size: {panels[0].get_content_width()}, {panels[0].get_content_height()} \
#                     Screen size: {scr.get_width()}, {scr.get_height()}"), lv.EVENT.SIZE_CHANGED, None)

locations = [
    lv.ALIGN.TOP_LEFT,
    lv.ALIGN.TOP_RIGHT,
    lv.ALIGN.BOTTOM_LEFT,
    lv.ALIGN.BOTTOM_RIGHT
    ]

sections = {}
conts = {}
groups = {}
encs = {}
for i, align in enumerate(locations):
    sections[i] = lv.obj(scr)
    sections[i].set_size(lv.pct(50), lv.pct(50))
    sections[i].align(align, 0, 0)
    sections[i].add_style(narrow_style, lv.STATE.DEFAULT)
    sections[i].set_scrollbar_mode(lv.SCROLLBAR_MODE.OFF)
    conts[i] = lv.obj(sections[i])
    conts[i].set_size(lv.pct(100), lv.pct(75))
    conts[i].align(lv.ALIGN.TOP_MID, 0, 0)
    conts[i].add_style(narrow_style, lv.STATE.DEFAULT)
    groups[i] = lv.group_create()
    encs[i] = EncoderWidget(sections[i], groups[i], width=lv.pct(100), height=lv.pct(25), alignment=(lv.ALIGN.BOTTOM_MID, 0, 0))

zmp = ZoomedMenuPanel(params=main_menu, parent=conts[0], src_group=groups[0], root=True, title="ZMP", icon=None)
zlp = ZoomedLivePanel(params=live_panels, parent=conts[1], src_group=groups[1], root=True, title="ZLP", icon=None)
rmp = RoundMenuPanel(params=main_menu, parent=conts[2], src_group=groups[2], root=True, title="RMP", icon=None)
fflp = FlexFlowLivePanel(params=live_panels, parent=conts[3], src_group=groups[3], root=True, title="FFLP", icon=None)

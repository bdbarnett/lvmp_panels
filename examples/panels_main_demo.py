#!/opt/bin/lv_micropython -i

# SPDX-FileCopyrightText: 2023 Brad Barnett
#
# SPDX-License-Identifier: MIT

import display_driver
import lvgl as lv
from sys import platform
from panels import ListMenuPanel, MatrixMenuPanel, RoundMenuPanel, ZRoundMenuPanel
from panels import CircularLivePanel, HorizontalLivePanel, VerticalLivePanel, TabViewLivePanel
from panels import IndevManager, config
from encoders import EncoderIRQ, EncoderDisplay
from panels_demo_data import main_menu, live_panels
from tools.style_finder import StyleFinder

def tvlp_wrapper(*args, **kwargs):
    """
    Wrapper around TabViewLivePanel to change the resolution on Linux to a 4x3 aspect ratio
    and create an encoder for the left-side buttons
    """
    if platform == 'linux':
        hor, ver = lv.disp_get_default().get_hor_res(), lv.disp_get_default().get_ver_res()
        lv.disp_get_default().set_res(ver*4//3, ver)
    panel = TabViewLivePanel(*args, **kwargs)
    if platform == 'linux':
        tv_encoder = EncoderDisplay(group=panel.group, title="TabView Encoder")
        panel.add_event(lambda e: [lv.disp_get_default().set_res(hor, ver), tv_encoder.delete()], lv.EVENT.DELETE, None)
    else:
        tv_encoder = EncoderIRQ(group=panel.group, pin_num_clk=None, pin_num_dt=None, pull_up=True, half_step=True)

def set_rotate(e):
    config.rotate = (e.get_target_obj().get_state() & lv.STATE.CHECKED > 0)
    print(f"{config.rotate}")

btn_defs = [
    ("List Menu", lambda e: ListMenuPanel(e, params=main_menu, parent=scr, title="Main Menu", idm=idm)),
    ("Matrix Menu", lambda e: MatrixMenuPanel(e, params=main_menu, parent=scr, title="Main Menu", idm=idm)),
    ("Round Menu", lambda e: RoundMenuPanel(e, params=main_menu, parent=scr, title="Main Menu", idm=idm)),
    ("ZRound Menu", lambda e: ZRoundMenuPanel(e, params=main_menu, parent=scr, title="Main Menu", idm=idm)),
    ("Rotate", set_rotate),
    ("Circular\nL Panel", lambda e: CircularLivePanel(e, params=live_panels, parent=scr, title="Live Menu", idm=idm)),
    ("Horizontal\nL Panel", lambda e: HorizontalLivePanel(e, params=live_panels, parent=scr, title="Live Menu", idm=idm)),
    ("Vertical\nL Panel", lambda e: VerticalLivePanel(e, params=live_panels, parent=scr, title="Live Menu", idm=idm)),
    ("TabView\nL Panel", lambda e: tvlp_wrapper(e, params=live_panels, parent=scr, title="Live Menu", idm=idm)),
    ]

if platform == 'linux': lv.disp_get_default().set_res(240, 240)

scr = lv.scr_act()

enc = EncoderDisplay() if platform == 'linux' else EncoderIRQ(pin_num_clk=10, pin_num_dt=11, pull_up=True, half_step=True)
idm = IndevManager([enc.get_indev()])

btns = {}
for i, (text, item) in enumerate(btn_defs):
    x = (i % 3 - 1) * 33
    y = (i // 3 - 1) * 33
    btns[i] = lv.btn(scr)
    btns[i].set_size(lv.pct(30), lv.pct(30))
    btns[i].align(lv.ALIGN.CENTER, lv.pct(x), lv.pct(y))
    btns[i].set_style_bg_img_src(lv.SYMBOL.HOME, 0)
    btns[i].set_style_bg_color(lv.palette_main(lv.PALETTE.GREEN), lv.STATE.FOCUSED)
    btns[i].add_event(item, lv.EVENT.SHORT_CLICKED, None)
    label = lv.label(btns[i])
    label.set_text(text)
    label.align(lv.ALIGN.BOTTOM_MID, 0, 0)    

btns[4].add_flag(lv.obj.FLAG.CHECKABLE)
# sf = StyleFinder()
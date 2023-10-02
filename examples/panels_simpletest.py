#!/opt/bin/lv_micropython -i

# SPDX-FileCopyrightText: 2023 Brad Barnett
#
# SPDX-License-Identifier: MIT

import display_driver
import lvgl as lv
import panels
from panels_demo_data import live_panels as menu
from encoders import EncoderDisplay

# panels.config.panel_style_key = panels.styles.ROUND

enc = EncoderDisplay()
idm = panels.IndevManager([enc.get_indev()])
enc.style_key = panels.styles.DEFAULT
panels.add_styles_to_children(enc)

p = panels.TabViewLivePanel(params=menu, parent=lv.scr_act(), idm=idm, root=True)
tv_enc = EncoderDisplay(group=p.group, title="Tabview Encoder")

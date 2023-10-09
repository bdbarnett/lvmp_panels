# SPDX-FileCopyrightText: 2023 Brad Barnett
#
# SPDX-License-Identifier: MIT

import lvgl as lv
from . import styles
from tools import animations, events
from tools.misc import do_nothing
from sys import platform

panel_style_key = styles.styles.ROUND
rotate = False
default_icon = lv.SYMBOL.HOME
close_btn_icon = lv.SYMBOL.LEFT
close_btn_label = "Back"
default_obj_size = (lv.pct(66), lv.pct(66))

animation = animations.spin_grow if platform == 'linux' else None

# The following are pointers to functions.
# Any of them can be set to = do_nothing.
apply_styles = styles.apply_styles
default_callback = events.debug_event_cb
# warn = print
warn = do_nothing

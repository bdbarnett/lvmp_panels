# SPDX-FileCopyrightText: 2023 Brad Barnett
#
# SPDX-License-Identifier: MIT

import lvgl as lv
from . import styles
from tools import animations, events
from tools.misc import do_nothing

animation = animations.spin_grow
default_callback = events.debug_event_cb
rotate = True
panel_style_key = styles.ROUND


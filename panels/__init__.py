# SPDX-FileCopyrightText: 2023 Brad Barnett
#
# SPDX-License-Identifier: MIT

import lvgl as lv
from styles import styles, add_styles, add_styles_to_children
from . import config
from tools.indevs import IndevManager, add_children_to_group
from .base_panels import (
    _BasePanel,
    CustomPanel,
)
from .widget_panels import (
    AnalogClockPanel,
    ArcPanel,
    BtnMatrixPanel,
    BtnPanel,
    CalendarPanel,
    ColorWheelPanel,
    LabelPanel,
    ListPanel,
    RollerPanel,
    SliderPanel,
    TextAreaPanel,
)
from .menu_panels import (
    ListMenuPanel,
    MatrixMenuPanel,
    RoundMenuPanel,
    ZRoundMenuPanel,
)
from .live_panels import(
    CircularLivePanel,
    HorizontalLivePanel,
    VerticalLivePanel,
    TabViewLivePanel,
)
from .keypad import KeypadPanel, KeypadDisplay

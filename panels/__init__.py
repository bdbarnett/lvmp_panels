# SPDX-FileCopyrightText: 2023 Brad Barnett
#
# SPDX-License-Identifier: MIT

import lvgl as lv
import styles
from . import config
apply_styles = config.apply_styles
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

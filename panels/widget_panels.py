# SPDX-FileCopyrightText: 2023 Brad Barnett
#
# SPDX-License-Identifier: MIT

import lvgl as lv
import time  # for AnalogClockPanel and CalendarPanel
from . import add_styles_to_children, add_children_to_group
from .base_panels import _BasePanel
from tools.animations import Animation
from tools.misc import make_square


class AnalogClockPanel(_BasePanel):
    auto_add_title = False
    # title_align=(lv.ALIGN.TOP_LEFT, 0, 0)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        start_time = self.params
        HOUR, MIN, SEC = 0, 1, 2

        self.clock_res = (
            6  # Resolution (number of "subticks" per tick), must be an integer > 0
        )
        scale = self.clock_res * 60  # "subticks" per cycle

        self.obj_size = None
        # Create the meter
        self.obj = meter = lv.meter(self)
        self.obj.set_size(lv.pct(100), lv.pct(100))
        make_square(self.obj)
        self.obj.center()

        # Add the scales
        meter.set_scale_ticks(61, 1, 5, lv.palette_main(lv.PALETTE.GREY))
        meter.set_scale_major_ticks(5, 2, 10, lv.color_black(), -20)
        meter.set_scale_range(0, scale, 360, 270)

        # Create the indicators
        indic_sec = lv.meter_indicator_t()
        indic_min = lv.meter_indicator_t()
        indic_hour = lv.meter_indicator_t()

        # Add a needle line indicator
        indic_sec = meter.add_needle_line(1, lv.palette_main(lv.PALETTE.RED), -6)
        indic_min = meter.add_needle_line(2, lv.color_black(), 0)
        indic_hour = meter.add_needle_line(4, lv.color_black(), -20)

        # Redraw the text labels
        meter.add_event(self.tick_label_event, lv.EVENT.DRAW_PART_BEGIN, None)

        # Create an animation to set the seconds value
        anim_sec = Animation(
            indic_sec,
            lambda a, v: meter.set_indicator_value(indic_sec, v % scale),
            0,
            scale - 1,
            120_000,
            repeat_cnt=lv.ANIM_REPEAT_INFINITE,
            get_value_cb=lambda x: self.format_time(start_time)[SEC],
        )

        # Create an animation to set the minutes value
        anim_min = Animation(
            indic_min,
            lambda a, v: meter.set_indicator_value(indic_min, v % scale),
            0,
            scale - 1,
            7_200_000,
            repeat_cnt=lv.ANIM_REPEAT_INFINITE,
            get_value_cb=lambda x: self.format_time(start_time)[MIN],
        )

        # Create an animation to set the hours value
        anim_hour = Animation(
            indic_hour,
            lambda a, v: meter.set_indicator_value(indic_hour, v % scale),
            0,
            scale - 1,
            86_400_000,
            repeat_cnt=lv.ANIM_REPEAT_INFINITE,
            get_value_cb=lambda x: self.format_time(start_time)[HOUR],
        )

        # Start the animations and save them in a self.animations to be deleted by .__del__() in .go_back()
        self.animations = [anim_hour.start(), anim_min.start(), anim_sec.start()]

        self.finalize()

    def tick_label_event(self, e):
        draw_part_dsc = e.get_draw_part_dsc()

        # Be sure it's drawing meter related parts
        if draw_part_dsc.class_p != lv.meter_class:
            return

        # Be sure it's drawing the ticks
        if draw_part_dsc.type != lv.meter.DRAW_PART.TICK:
            return

        # Be sure it's a major tick
        if draw_part_dsc.id % 5:
            return

        # The order of numbers on the clock is tricky: 12, 1, 2, 3...
        if draw_part_dsc.id == 0:
            draw_part_dsc.text = "12"
        else:
            draw_part_dsc.text = str(draw_part_dsc.id // 5)

    def format_time(self, clock_time):
        res = self.clock_res
        if not clock_time: clock_time = time.localtime()[3:6]
        hour, min, sec = clock_time
        sec = (sec * res) % (res * 60)
        min = ((min * res) + (sec / 60)) % (res * 60)
        hour = ((hour * 5 * res) + (min / 12)) % (res * 60)
        return (int(hour), int(min), int(sec))


class ArcPanel(_BasePanel):
    title_align = (lv.ALIGN.CENTER, 0, 0)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        val, range = self.params if self.params else (50, (0, 99))
        value = val if type(val) == int else val()

        self.obj_size = None
        self.obj = obj = lv.arc(self)
        obj.set_size(lv.pct(66), lv.pct(66))
        make_square(obj)
        obj.center()
        obj.set_rotation(135)
        obj.set_bg_angles(0, 270)
        obj.set_range(*range)
        obj.set_value(value)
        label = lv.label(self)

        obj.add_event(
            lambda e: self.value_changed_event_cb(
                e, e.get_target_obj(), label, self.callback
            ),
            lv.EVENT.VALUE_CHANGED,
            None,
        )
        obj.add_event(
            lambda e: self.value_changed_event_cb(None, obj, label, None),
            lv.EVENT.STYLE_CHANGED,
            None,
        )

        self.finalize()

    def value_changed_event_cb(self, e, obj, label, callback):
        txt = "{:d}".format(obj.get_value())
        label.set_text(txt)

        # Rotate the label to the current pos of the arc
        obj.rotate_obj_to_angle(label, -30)

        if callback:
            callback(e)


class BtnPanel(_BasePanel):
    auto_add_title = False

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.obj = obj = lv.btn(self)
        obj.set_style_bg_img_src(self.icon, 0)

        if self.title:
            label = lv.label(obj)
            label.set_text(self.title)
            label.align(lv.ALIGN.CENTER, 0, 20)

        obj.add_event(self.callback, lv.EVENT.SHORT_CLICKED, None)

        self.finalize()


class BtnMatrixPanel(_BasePanel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        btn_map, ctrl_map, one_checked = self.params
        self.obj = obj = lv.btnmatrix(self)
        obj.set_map(btn_map)
        obj.set_ctrl_map(ctrl_map)
        obj.set_one_checked(one_checked)
        obj.set_selected_btn(0)

        obj.add_event(self.event_cb, lv.EVENT.VALUE_CHANGED, None)

        self.finalize()

    def event_cb(self, event):
        if type(self.callback) is list:
            self.callback[event.get_target_obj().get_selected_btn()](event)
        else:
            self.callback(event, event.get_target_obj().get_selected_btn())


class CalendarPanel(_BasePanel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.params:
            year, month, day = self.params
        else:
            year, month, day = time.localtime()[0:3]
#        date = lv.calendar_date_t({"year": year, "month": month, "day": day})
        self.obj = obj = lv.calendar(self)
        obj.set_showed_date(year, month)
        obj.set_today_date(year, month, day)
        # day_names=["S", "M", "T", "W", "T", "F", "S"]
        # obj.set_day_names(day_names)
        header=lv.calendar_header_arrow(obj)
        # header=lv.calendar_header_dropdown(obj)
        add_styles_to_children(header)
        cal_btns = obj.get_btnmatrix()
        add_styles_to_children(cal_btns)
        obj.clear_flag(obj.FLAG.CLICKABLE)
        self.group.add_obj(cal_btns)
        add_children_to_group(header, self.group)

        obj.add_event(self.value_changed_event_cb, lv.EVENT.VALUE_CHANGED, None)

        self.finalize()

    def value_changed_event_cb(self, e):
        obj = e.get_target_obj()

        date = lv.calendar_date_t()
        self.obj.get_pressed_date(date)
        self.obj.set_highlighted_dates([date], 1)

        self.callback(e)


class ColorWheelPanel(_BasePanel):
    title_align = (lv.ALIGN.CENTER, 0, 0)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        val = self.params if self.params else lv.palette_main(lv.PALETTE.GREEN)
        color = val if type(val) == lv.color32_t else val()

        self.obj_size = None
        self.obj = obj = lv.colorwheel(self, True)
        obj.set_size(lv.pct(66), lv.pct(66))
        obj.center()
        make_square(obj)
        obj.set_hsv(color.color_to_hsv())

        obj.add_event(self.callback, lv.EVENT.VALUE_CHANGED, None)

        self.finalize()


class LabelPanel(_BasePanel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.txt, refresh = self.params if self.params else ("Label", False)
        self.obj_size = None
        is_str = isinstance(self.txt, str)

        self.obj = obj = lv.label(self)
        obj.center()
        obj.add_flag(lv.obj.FLAG.CLICKABLE)

        if refresh:
            timer = lv.timer_create_basic()
            self.timers.append(timer)
            timer.set_period(refresh)
            timer.set_repeat_count(-1)
            if is_str:
                timer.set_cb(lambda e: obj.set_text(self.txt))
            else:
                timer.set_cb(lambda e: obj.set_text(self.txt()))
        else:
            if is_str:
                obj.set_text(self.txt)
            else:
                obj.set_text(self.txt())

        self.finalize()


class ListPanel(_BasePanel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        option_list = self.params if self.params else None
        self.obj = obj = lv.list(self)
        obj.clear_flag(lv.obj.FLAG.CLICKABLE)

        for item in option_list:
            if type(item) == str:
                obj.add_text(item)
            else:
                self.add_item(*item)

        self.finalize()

    def add_item(self, title, icon, func):
        btn = self.obj.add_btn(icon, title)
        if func is None:
            func = self.callback
        btn.add_event(
            lambda e: func(e, title=title),
            lv.EVENT.SHORT_CLICKED,
            None,
        )
        self.group.add_obj(btn)


class RollerPanel(_BasePanel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        select, option_list = self.params if self.params else (1, "1\n2\n3\n4\n5\n")
        selected = select if type(select) == int or select == None else select()
        self.obj = obj = lv.roller(self)
        obj.set_options("\n".join(option_list), lv.roller.MODE.INFINITE)
        obj.set_visible_row_count(3)
        if selected: obj.set_selected(selected, lv.ANIM.ON)

        obj.add_event(self.callback, lv.EVENT.VALUE_CHANGED, None)

        self.finalize()


class SliderPanel(_BasePanel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        val, range = self.params if self.params else (50, (0, 99))
        value = val if type(val) == int else val()
        
        self.obj_size = (lv.pct(80), lv.pct(10))
        self.obj = obj = lv.slider(self)
        obj.set_range(*range)
        obj.set_value(value, lv.ANIM.OFF)
        label = lv.label(self)
        label.align(lv.ALIGN.CENTER, 0, lv.pct(-15))

        obj.add_event(
            lambda e: self.value_changed_event_cb(
                e, e.get_target_obj(), label, self.callback
            ),
            lv.EVENT.VALUE_CHANGED,
            None,
        )
        # Manually update the label for the first time
        self.value_changed_event_cb(None, obj, label, None)

        self.finalize()

    def value_changed_event_cb(self, e, obj, label, callback):
        txt = "{:d}".format(obj.get_value())
        label.set_text(txt)

        if callback:
            callback(e)


class TextAreaPanel(_BasePanel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        param = self.params if self.params else None

        self.obj = obj = lv.textarea(self)

        obj.set_one_line(False)
        obj.set_cursor_click_pos(False)

        obj.add_event(self.callback, lv.EVENT.READY, None)

        if type(param) == str:
            obj.set_text(param)
            self.source = None
        elif param == None:
            self.source = None
        else:
            self.source = param(obj)

        self.finalize()

    def _del(self):
        if self.source: self.source._del()
        super()._del()

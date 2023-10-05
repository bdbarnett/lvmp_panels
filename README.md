# lvmp_panels
Panels is a framework to aid in rapid creation of GUIs using LVGL on Micropython.
Check out the [screenshots](assets/README.md).

## Goals
The goal of Panels is to provide a framework to allow quickly creating GUIs in [lv_micropython](https://github.com/lvgl/lv_micropython), freeing up resources to focus on the other aspects of a project.
- Must work on small round displays, which can be challenging since things like a title bar, status bar and "window controls" aren't visible on a round screen.
- Must work with both touchscreens and non-touchscreens alike, utilizing LVGL's indev (input device) interfaces for rotary encoders and keypads.
- Must be easy to apply styles to maintain a consistent look and feel.
- Must provide a polished look and feel without relying on graphics.

### A Quick Example
```
import display_driver
import lvgl as lv
import panels
panel = panels.AnalogClockPanel(parent=lv.scr_act(), root=True)
```
![AnalogClockPanel.png](assets/AnalogClockPanel.png)

## Recommended hardware
Panels is designed to work on any display with 240x240 resolution or greater.  It is recommended to have external PSRAM in addition to the microcontroller's RAM, such as most ESP32-S3 boards, but should work fine on devices with 256KB RAM or more.  Development is done on Windows Subsystem for Linux using the Unix port of lv_micropython.  It is not recommended to use a device with only 128KB RAM, such as the Raspberry Pi Pico, but it may work for small displays with only a panel or two on Pico.  Storage requirements are negligible, with the exception of space for the binaries provided by you.  That is to say, any device capable of running LVGL Micropython should have enough storage to house the framework.  It is possible, and a goal of Panels, to create GUIs that don't use any external graphics.

## Uses
Panels may be used in any microcontroller project that supports Micropython with LVGL bindings and has drivers for the display.  Touchscreen drivers are very beneficial, but not required if using an encoder or keypad.  Example use cases are watches, clocks, CNC machine controls, thermostats, vehicle instrumentation, digital musical instruments, and much more.  Multiple panels can be used per display, and multiple displays may be used if the hardware supports them.

## Dependencies
While creating Panels, I realized many of the classes and functions needed could also be used in other LVGL Micropython projects that don't use Panels.  When possible, these classes and functions were moved outside of Panels into the projects below.
- [lvmp_tools](https://github.com/bdbarnett/lvmp_tools): A collection of modules providing functions related to a particular idea.  Several of these were used by the writer to aid in troubleshooting, discovery and learning during the process of creating Panels, such as `flags.py`, `parts.py` and `states.py`.  Others provide functionality that will be useful in many scenarios, such as `ImageCache` in `images.py`, `default_event_cb` callback in `events.py` and `IndevManager` in `indevs.py`.
- [lvmp_styles](https://github.com/bdbarnett/lvmp_styles): Provides a single function, `apply_styles`, and a mechanism for applying styles selectively or automatically.  Styles is not meant to replace themes in LVGL, but is meant to provide a different means for defining and applying styles.
- [lvmp_encoders](https://github.com/bdbarnett/lvmp_encoders): Classes that provide drivers for hardware encoders, a widget to emulate an encoder and a display object containing the widget for unix to make it easier to design and troubleshoot interfaces that use encoders without having a physical encoder.
- [lvmp_keypads](https://github.com/bdbarnett/lvmp_styles): Similar to Encoders.  A work in progress.  Class drivers for hardware and simulated hardware keypads.

## Groups and Input Devices
LVGL has a mechanism for assigning input devices (indevs) like rotary encoders and keypads to a group, where the objects in a group can be navigated with those input devices.  Where objects are created to take the display space of other objects, the built-in mechanism for indev management can be difficult to manage manually, so Panels uses the `IndevManager` class from `tools.indevs` to handle this management automatically.  If no encoders or keypads are used in a project, no `IndevManager` is needed.  However, any project that uses those types of indevs should create one `IndevManager` per root panel.  That panel will handle handing the indev manager to child panels.  The default group `lv.group_get_default()` is never used in Panels.  Instead, each panel creates its own group, or, as in the case of some LivePanels, child panels use the group owned by their parent.

## Callbacks
GUIs in general and LVGL specifically rely heavily on callbacks.  A callback is a function that is executed when a particular event happens, for example when a button is pushed or an object gains focus.  LVGL, and thus Panels, will work with normal Micropython functions.  However, Python and Micropython provide `lambda` functions that allow quickly creating an action without defining a named function.  It is beyond the scope of this document to teach the use of `lambda` functions, but it is greatly encouraged to learn and use them with Panels.  The examples are a great resource for discovering the use of lambdas.

## Usage
Panels are Micropython classes.  All panels are either subclassed directly from the `_BasePanel` class, or are sublasses of other classes that are themselves subclasses of `_BasePanel`.  `_BasePanel` is subclassed from `lv.obj`.  Panels provides 4 types of panel classes:
- WidgetPanels: Provide the majority of useful information, such as lists, clocks, calendars, arcs and sliders.
- MenuPanels: Have buttons to launch other panels or execute callback functions. Menu items are not launched, or opened, until the button is pushed.  This saves on resources because the items are only loaded one at a time.
- LivePanels: Panels that contain other panels.  A LivePanel launches all of the item panels at once, even though only one panel may be visible at a time.
- `CustomPanel`: This is a subclass of `_BasePanel` meant to make it easier for you to create your own panels.  See Extensibility below.

## Extensibility
The `CustomPanel` class can be used in two ways.  First, you may define a function that is called to populate the `CustomPanel`.  That function is passed as a paramenter to `CustomPanel` and executed when the panel is loaded, allowing `CustomPanel` to handle styling, adding a title and back buttons, and managing input devices and groups, while letting the function handle adding widgets and handling the program logic.  The second option is to subclass either `_BasePanel` or `CustomPanel`.  See the checkboxes, switches and sliders functions in the examples for more details on the first method.  See `NavPanel` in the examples and all the classes in `widgetpanels.py` for the second method.

## Customization
Interfaces created using Panels may be customized by editing `styles.py` and `style_defs.py` in the `styles` directory, and by editing `config.py` in the `panels` directory.  Panels are defined as classes so they may be subclassed and have class variables or methods overridden.

## Contributing
Contributions are both welcome and encouraged.  We don't have a formal contributions policy yet, and the author is in the process of learning Github.  For now, we ask that contributions not change the API of the classes and functions without very good reason, and that all code modifications first be tested on the unix port of lv_micropython.

## Acknowledgements
This work would not be possible without the fantastic work, including hundreds of developers and counless hours, on the LVGL and Micropython projects.  Many of the examples in this project are based on the Micropython examples at [docs.lvgl.io](https://docs.lvgl.io). The REPL example is based on the work of [boochow](https://github.com/boochow/FBConsole) and [JohnieBraaf](https://github.com/JohnieBraaf/Boat-Controller-Micropython-LVGL/blob/main/console.py).  Example images are from [Icons8](https://icons8.com).


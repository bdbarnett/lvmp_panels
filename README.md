# lvmp_panels
Panels is a framework to aid in rapid creation of GUIs using LVGL on Micropython

## Goals
The goal of Panels is to provide a framework to allow quickly creating GUIs, freeing up resources to focus on the other aspects of a project.
- Must work with small round displays, which can be challenging to fit since things like a title bar, status bar, and "window controls" aren't visible on a round screen
- Must work with both touchscreens and non-touchscreens alike, utilizing LVGL's indev (input device) interfaces for rotary encoders and keypads
- Must be easy to apply styles to maintain a consistent look and feel
- Must provide a polished look and feel without relying on graphics

## Recommended hardware
Panels is designed to work on any display with 240x240 resolution or greater.  It is recommended to have external PSRAM in addition to the microscontroller's RAM, such as an ESP32-S3 with additional PSRAM, but should work fine on devices with 256KB RAM or more.  It is not recommended to use a device with only 128KB RAM, such as the Raspberry Pi Pico, but it should work for small displays with only a panel or two on Pico.  Storage requirements are negligible, with the exception of the binaries you provide.  That is to say, any device capable of running LVGL Micropython should have enough storage to house the framework.  The only storage requirement is the space for your assets, like icons and graphics.  It is possible, and a goal of Panels, to create GUIs that don't use any external graphics.

## Uses
Panels may be used in any microcontroller project that supports Micropython with LVGL bindings and has drivers for the display.  Touchscreen drivers are very beneficial, but not required if using an encoder or keypad.  Example use cases are watches, clocks, CNC machine controls, thermostats, vehicle instrumentation, digital musical instruments, and much more.  Multiple panels can be used per display, and multiple displays may be used if the hardware supports them.

## Dependencies
While creating Panels, it was realized that many of the clases and functions needed could also be used in other LVGL Micropython projects that don't use Panels.  When possible, these classes and functions were moved outside of Panels into the projects below.
        - tools - a collection of modules providing functions related to a particular idea.  Several of these were used by the writer to aid in troublshooting, discovery and learning during the process of creating panels, such as flags.py, parts.py and states.py.  Others provide functionality that will be useful in many scenarios, such as the ImageCache in images.py and the default_event_cb callback in events.py and IndevManager in indevs.py.
        - styles - provides a single function, apply_styles, and a mechanism for applying styles selectively or automatically.  
        - encoders.py - classes that drivers for hardware encoders, a widget to emulate an encoder and a display object for unix to make it easier to design and troubleshoot interfaces that use encoders without having a physical encoder.
        - keypads - a work in progress for hardware and simulated hardware keypads

## Groups and Input Devices
LVGL has a mechanism for assigning input devices (indevs) like rotary encoders and keypads to a group, where the objects in a group can be navigated with those input devices.  Where objects are created to take the display space of other objects, the built-in mechanism for indev management can be difficult to manage manually, so Panels uses the IndevManager class in tools.indevs to handle this management automatically.  If no encoders or keypads are used in a project, no IndevManager is needed.  However, any project that uses those types of indevs should create one IndevManager per root panel.  That panel will handle handing the indev manager to child panels.  In panels, the default group (lv.group_get_default()) is never used.  Instead, each panel creates its own group, or, as in the case of some of the LivePanels, the child panels use the group owned by their parent.

## Callbacks
GUIs in general and LVGL specifically rely heavily on callbacks.  A callback is function that is executed when a particular event happens, for example when a button is pushed or an object gains focus.  LVGL, and thus panels, will work with normal Micropython functions.  However, Python and Micropython provide lambda functions that allow quickly creating an action without defining a named function.  It is beyond the scope of this document to teach the use of lambda functions, but it is greatly encouraged to learn and use them with Panels.  The examples are a great resource for discovering the use of lambdas.

## Usage
Panels are Micropython classes.  All panels are either subclassed directly from the _BasePanel class, or are sublasses of other classes that are themselves subclasses of _BasePanel.  _BasePanel is subclassed from lv.obj.  Panels provides 4 types of panel classes:
        - WidgetPanels - provide the majority of useful information, such as lists, clocks, calendars, arcs and sliders
        - MenuPanels - have buttons to launch other panels or execute callback functions. Menu items are not launched, or opened, until the button is pushed.  This saves on resources because the items are only loaded one at a time.
        - LivePanels - Panels that contain other panels.  The LivePanel launches all of the item panels at once, even though only one panel may be seen at a time.
		    - CustomPanel - This is a subclass of _BasePanel meant to make it easier for you to create your own panels.  See Extensibility below.

## Extensibility
The CustomPanel class can be used in two ways.  Firstly, you may define a function that is called to populate the CustomPanel.  That function is passed as a paramenter to CustomPanel and executed when the panel is loaded, allowing CustomPanel to handle styling, adding a title and back buttons, and managing input devices and groups, while letting the function handle adding widgets and handling the program logic.  The second option is to subclass either _BasePanel or CustomPanel.  See the checkboxes, switches and sliders functions in the examples for more details on the first method.  See NavPanel in the examples and all the classes in WidgetPanels.py for the second method.

## Customization
Interfaces created using Panels may be customized by editing styles.py and style_defs.py from the styles package, and by editing config.py in the panels directory.  Panels are defined as classes so they may be subclassed and have class variables or methods overridden.

## Contributing
Contributions are both welcome and encouraged.  We don't have a formal contributions policy yet, and the author is in the process of learning Github.  For now, we ask that contributions not change the API of the classes and functions without very good reason, and that all code modifications first be tested on the unix port of lv_micropython.

## Acknowledgements
This work would not be possible without the fantastic work, including hundreds of developers and counless hours, on the LVGL and Micropython projects.  Many of the examples in this project are based on the Micropython examples at docs.lvgl.io. The REPL example is based on the work of boochow and JohnieBraaf.

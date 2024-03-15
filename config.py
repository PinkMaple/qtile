# Matilda Väliaho 2023

import os, subprocess, re

from libqtile import bar, layout, widget, hook
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy

mod = "mod4"

#
#   Default settings
# 

wallpaper = "~/.config/qtile/desktop3.jpg"

# Apps:
terminal = "kitty"
browser = "firefox"
file_explorer = "nemo"
editor = "code"
screenshot = "flameshot gui"
taskmanager = "kitty htop"
sound_controller = "pavucontrol"
log_screen = "light-locker-command -l"



#
#   Keybindings
#

keys = [

    Key([mod], "l", lazy.spawn(log_screen), desc="Logs screen"),

    Key([mod], "Left", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "Right", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "Down", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "Up", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),


    Key([mod, "shift"], "Left", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "Right", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "Down", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "Up", lazy.layout.shuffle_up(), desc="Move window up"),


    Key([mod, "control"], "Left", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "Right", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "Down", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "Up", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),

    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),

    Key([mod], "t", lazy.spawn(terminal), desc="Launch terminal"),

    Key([mod], "q", lazy.window.kill(), desc="Kill focused window"),
    Key([mod], "f", lazy.window.toggle_floating(), desc="Toggle floating on the focused window"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "r", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),
    Key([mod, "shift"], "s", lazy.spawn(screenshot), desc="Take a screenshot")
    
]




#
#   Groups
#

groups = [
    Group("1", label="main"),
    Group("2", label="web", layout="max"),
    Group("3", label="dev"),
    Group("4", label="chat"),
    Group("5", label="other"),
]

for i in groups:
    keys.extend(
        [
            Key(
                [mod],
                i.name,
                lazy.group[i.name].toscreen(),
                desc="Switch to group {}".format(i.name),
            ),
            Key(
                [mod, "shift"],
                i.name,
                lazy.window.togroup(i.name, switch_group=False),
                desc="Switch to & move focused window to group {}".format(i.name),
            ),
        ]
    )


#
#   Layouts
#

layouts = [
    layout.Columns(
        border_focus="#F75F5F",
        border_normal="#875F5F",
        border_width=4,
        margin=4
    ),
    layout.Max(),
    layout.Floating(),
    layout.Zoomy(),
]


widget_defaults = dict(
    font="sans",
    fontsize=12,
    padding=4,
)
extension_defaults = widget_defaults.copy()





#
#   COLOURS 
#

colours = [
    "#8354b3",       # First background Colour
    "#F0F0F0",       # Second background Colour
    "#1F1F1F",       # Third background Colour
    "#F1C40F",       # Fourth background Colour

    "F0F0F0",        # Active group colour
    "202020",        # Inactive group colour
    "000000",        # Window Name

    "5FAF1F",        # CPU colour
    "53C4b3",        # Memory colour
    "236473",        # Bluetooth battery colour

]



#
#   SCREEN
#

def get_bluetooth_battery():
    stream = os.popen('bluetoothctl info')
    output = stream.read()

    battery_output = output.split("Battery Percentage:")

    if len(battery_output) > 1:
        battery = battery_output[1]
        return re.findall(r'\((.*?)\)', battery)[0] + "% 🔋"

    return ""


def GetBar(main_bar):

    top_bar = [
        widget.TextBox("🐝", background = colours[0],
            mouse_callbacks = {"Button1" : lazy.spawn("jgmenu_run")}
        ),
        widget.GroupBox(
            background = colours[0],
            active= colours[4],
            inactive=colours[5],
                    
            highlight_method="line",
            highlight_color=["#530483", "#8354b3"],
            this_current_screen_border=colours[3],
            disable_drag=True,
        ),
        widget.Spacer(background = colours[0], length=150),
        widget.CurrentLayoutIcon(foreground=colours[4], background=colours[0], scale=0.8),
        widget.CurrentLayout(foreground=colours[4], background=colours[0]),
        widget.TextBox("◥", fontsize=40, padding=-7, foreground=colours[1], background = colours[0]),
        widget.WindowName(
            foreground=colours[6],
            background=colours[1],
            format="🔶 {state} {name:.50} 🔶",
            scroll_fixed_width=True,
            width=420,
        ),
        widget.TextBox("◣", fontsize=40, padding=-7, foreground=colours[1], background = colours[2]),
        widget.Spacer(background = colours[2]),
        widget.Clock(format="%Y-%m-%d %a %H:%M", background=colours[2]),
        widget.CPU(
            foreground=colours[7],
            background=colours[2],
            format="CPU {load_percent:0>4}% ",
            mouse_callbacks = {"Button1" : lazy.spawn(taskmanager)},
        ),
        widget.Memory(
            foreground=colours[8],
            background=colours[2],
            format="Mem: {MemPercent:0>4}% ",
            mouse_callbacks = {"Button1" : lazy.spawn(taskmanager)},
        ),
        widget.TextBox("◥", fontsize=40, padding=-7, foreground=colours[3], background = colours[2]),
        widget.Spacer(background = colours[3], length=320),
        
        widget.TextBox(
            "🔊", 
            mouse_callbacks = {"Button1" : lazy.spawn(sound_controller)},
            background=colours[3]
        ), 
        widget.QuickExit(default_text="⏻ ", padding=10, countdown_format="{}", foreground=colours[2], background=colours[3]),
    ]

    if main_bar: 
        top_bar.insert(2, widget.Prompt(
            background = colours[0],
            foreground=colours[4],
            prompt=">>> "
        ))
        top_bar.insert(15, widget.GenPollText(
            func = get_bluetooth_battery,
            background = colours[3],
            foreground= colours[9],
            update_interval = 100,
        ))
        top_bar.insert(17, widget.Systray(background=colours[3]))
    return bar.Bar(top_bar, 24, opacity=0.8, margin=[4,10,0,10]) #N E S W




screens = [
    Screen(
        wallpaper = wallpaper,
        wallpaper_mode = "fill",
        top=GetBar(False),
    ),
    Screen(
        wallpaper = wallpaper,
        wallpaper_mode = "fill",
        top=GetBar(True),
    )
]


# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]





#
#   Floating apps
#

floating_layout = layout.Floating(
    float_rules=[
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ss h-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
        #Match(wm_class="pavucontrol"),
    ]
)





#
#   Other settings
#

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
floats_kept_above = True
cursor_warp = False

auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True
auto_minimize = True


@hook.subscribe.startup_once
def autostart():
    home = os.path.expanduser('~/.config/qtile/autostart.sh')
    subprocess.call([home])


wmname = "LG3D"

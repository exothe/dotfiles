# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from libqtile import bar, layout, widget
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
from libqtile.backend.wayland import InputConfig

mod = "mod4"
terminal = guess_terminal()

@lazy.window.function
def move_floating_window(w, x: int = 0, y: int = 0):
    if w.floating:
        w.set_position_floating(w.float_x + x, w.float_y + y)

@lazy.window.function
def resize_floating_window(w, width: int = 0, height: int = 0):
    if w.floating:
        w.set_size_floating(w.width + width, w.height + height)

floating_move_size = 50 # the amount that floating windows will be moved or resized per key press

keys = [
    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html
    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.screen.toggle_group(), desc="Go to the last used group"),
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),

    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key(
        [mod, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "r", lazy.spawn("wofi -S run"), desc="Spawn a command using a prompt widget"),

    # custom mappings
    Key([mod], "f", lazy.window.toggle_floating(), desc="Toggle floating"),
    Key([mod], "c", lazy.spawn("open_special_file.sh"), desc="Open some a special file"),

    # floating windows beinding
    Key([mod], "Left", move_floating_window(x=-floating_move_size), desc="Grow window to the left"),
    Key([mod], "Right", move_floating_window(x=floating_move_size), desc="Grow window to the right"),
    Key([mod], "Down", move_floating_window(y=floating_move_size), desc="Grow window down"),
    Key([mod], "Up", move_floating_window(y=-floating_move_size), desc="Grow window up"),
    Key([mod, "control"], "Left", resize_floating_window(width=-floating_move_size), desc="Grow window to the left"),
    Key([mod, "control"], "Right", resize_floating_window(width=floating_move_size), desc="Grow window to the right"),
    Key([mod, "control"], "Down", resize_floating_window(height=floating_move_size), desc="Grow window down"),
    Key([mod, "control"], "Up", resize_floating_window(height=-floating_move_size), desc="Grow window up"),

    # Audio and brigthness fn keys
    Key([], "XF86AudioRaiseVolume", lazy.spawn('amixer -q sset Master 5%+'), desc='Increase volume'),
    Key([], "XF86AudioLowerVolume", lazy.spawn('amixer -q sset Master 5%-'), desc='Lower volume'),
    Key([], "XF86AudioMute", lazy.spawn('amixer -q sset Master toggle'), desc='Mute/unmute volume'),

    Key([], "XF86MonBrightnessUp", lazy.spawn('xbacklight -inc 5'), desc='Increase brigthness'),
    Key([], "XF86MonBrightnessDown", lazy.spawn('xbacklight -dec 5'), desc='Decrease brigthness'),

    # Screenshots
    Key([mod], "Print", lazy.spawn('grim'), desc="Take a screenshot from the entire screen"),
    Key([mod, "shift"], "Print", lazy.spawn('grim -g "$(slurp)"'), desc="Take a screenshot from a selection"),
]

groups = [Group(i) for i in "1234567890"]

for i in groups:
    keys.extend(
        [
            # mod1 + letter of group = switch to group
            Key(
                [mod],
                i.name,
                lazy.group[i.name].toscreen(),
                desc="Switch to group {}".format(i.name),
            ),
            # mod1 + shift + letter of group = switch to & move focused window to group
            Key(
                [mod, "shift"],
                i.name,
                lazy.window.togroup(i.name, switch_group=True),
                desc="Switch to & move focused window to group {}".format(i.name),
            ),
            # Or, use below if you prefer not to switch to that group.
            # # mod1 + shift + letter of group = move focused window to group
            # Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
            #     desc="move focused window to group {}".format(i.name)),
        ]
    )

layouts = [
    layout.Columns(border_focus_stack=["#d75f5f", "#8f3d3d"], border_width=4),
    layout.Max(),
    # Try more layouts by unleashing below layouts.
    # layout.Stack(num_stacks=2),
    # layout.Bsp(),
    # layout.Matrix(),
    # layout.MonadTall(),
    # layout.MonadWide(),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]

widget_defaults = dict(
    font="sans",
    fontsize=12,
    padding=3,
)
extension_defaults = widget_defaults.copy()

sep = widget.Sep(foreground='ffffff')

screens = [
    Screen(
        bottom=bar.Bar(
            [
                widget.CurrentLayout(),
                widget.GroupBox(),
                widget.Prompt(),
                widget.WindowName(),
                widget.Chord(
                    chords_colors={
                        "launch": ("#ff0000", "#ffffff"),
                    },
                    name_transform=lambda name: name.upper(),
                ),
                widget.Bluetooth(
                    fmt='Bluetooth: {}',
                    hci='/dev_94_DB_56_40_C8_41',
                    mouse_callbacks={'Button1': lazy.spawn('blueman-manager')},
                ),
                sep,
                widget.CPU(),
                sep,
                widget.Memory(),
                sep,
                widget.Wlan(
                    format='{essid} {percent:2.0%}',
                    interface='wlp7s0',
                    mouse_callbacks={'Button1': lazy.spawn("nm-connection-editor")},
                ),
                sep,
                widget.Backlight(
                    fmt='brigthness: {}',
                    change_command='save_xbacklight.sh {0} 5',
                    backlight_name='intel_backlight',
                    step=5,
                ),
                sep,
                widget.Volume(
                    mouse_callbacks={'Button1': lazy.spawn("pavucontrol")},
                    fmt='Vol: {}',
                    step=1,
                ),
                sep,
                # NB Systray is incompatible with Wayland, consider using StatusNotifier instead
                widget.StatusNotifier(),
                # widget.Systray(),
                widget.Clock(format="%I:%M:%S %p %a %d/%m/%Y"),
                widget.BatteryIcon(),
                widget.Battery(
                    charge_char="⚡",
                    discharge_char="↓",
                    format="{char} {percent:2.0%} {hour:d}h {min:02d}min {watt:.2f} W",
                    update_interval=30
                ),
                widget.QuickExit(),
            ],
            24,
            # border_width=[2, 0, 2, 0],  # Draw top and bottom borders
            # border_color=["ff00ff", "000000", "ff00ff", "000000"]  # Borders are magenta
        ),
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = {
    "type:touchpad": InputConfig(natural_scroll=True, tap=True),
    "type:keyboard": InputConfig(kb_layout="us", kb_variant="altgr-intl", kb_options="caps:ctrl_modifier"),
}

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"

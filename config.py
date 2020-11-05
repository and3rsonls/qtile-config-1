# Qtile Config File
# http://www.qtile.org/

# Sergio Ribera

# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from libqtile.config import Key, Screen, Group, Drag, Click
from libqtile.command import lazy
from libqtile import layout, bar, widget, hook
from libqtile.bar import Bar

from powerline.bindings.qtile.widget import PowerlineTextBox

from os import listdir
from os import path
import subprocess
import json

font = "Hack Nerd Font Mono"

qtile_path = path.join(path.expanduser("~"), ".config", "qtile")


# THEME

theme = "solarized-dark"  # only if available in ~/.config/qtile/themes

theme_path = path.join(qtile_path, "themes", theme)

# map color name to hex values
with open(path.join(theme_path, "colors.json")) as f:
    colors = json.load(f)

def only_color(color):
   return colors[color][0][1:]

# AUTOSTART
@hook.subscribe.startup_once
def autostart():
    script = path.join(qtile_path, "autostart.sh")
    subprocess.call([script])


# kick a window to another screen (handy during presentations)
def kick_to_next_screen(qtile, direction=1):
    other_scr_index = (qtile.screens.index(qtile.currentScreen) + direction) % len(qtile.screens)
    othergroup = None
    for group in qtile.cmd_groups().values():
        if group['screen'] == other_scr_index:
            othergroup = group['name']
            break
        if othergroup:
            qtile.moveToGroup(othergroup)


# KEYS

mod = "mod4"

#          Special  KeyCap  Actions
keys = [Key(key[0], key[1], *key[2:]) for key in [

    # Screen shots
    ([], "Print", lazy.spawn("xfce4-screenshooter")),
    # Full screen
    ([mod], "p", lazy.spawn("xfce4-screenshooter -f")),
    # Select area
    ([mod, "shift"], "p", lazy.spawn("xfce4-screenshooter -r")),
    # Active window
    ([mod, "control"], "p", lazy.spawn("xfce4-screenshooter -w")),

    # Change window sizes (MonadTall)
    ([mod, "shift"], "l", lazy.layout.grow()),
    ([mod, "shift"], "h", lazy.layout.shrink()),

    # Toggle floating
    ([mod, "shift"], "f", lazy.window.toggle_floating()),

    # kick to next/prev screen
    ([mod], "o", lazy.function(kick_to_next_screen)),
    ([mod, "shift"], "o", lazy.function(kick_to_next_screen, -1)),

    # Move windows up or down in current stack
    ([mod, "shift"], "j", lazy.layout.shuffle_down()),
    ([mod, "shift"], "k", lazy.layout.shuffle_up()),

    # Toggle between different layouts as defined below
    ([mod, "control"], "Tab", lazy.next_layout()),

    # Kill window
    ([mod], "q", lazy.window.kill()),

    # Restart Qtile
    ([mod, "control"], "r", lazy.restart()),

    ([mod, "control"], "q", lazy.shutdown()),

    # Switch window focus to other pane(s) of stack
    ([mod], "space", lazy.layout.next()),

    # Swap panes of split stack
    ([mod, "shift"], "space", lazy.layout.rotate()),

    ([], 'XF86Back', lazy.screen.prev_group(skip_managed=True, )),
    ([], 'XF86Forward', lazy.screen.next_group(skip_managed=True, )),
    ([mod], 'XF86Back', lazy.screen.prev_group(skip_managed=True, )),
    ([mod], 'XF86Forward', lazy.screen.next_group(skip_managed=True, )),
    ([mod], 'Left', lazy.screen.prev_group(skip_managed=True, )),
    ([mod], 'Right', lazy.screen.next_group(skip_managed=True, )),
    ([mod], 'Escape', lazy.screen.togglegroup()),

    # ------------ Apps Configs ------------

    # Menu
    ([mod], "m", lazy.spawn("rofi -show run")),

    # Window Nav
    ([mod], "Tab", lazy.spawn("rofi -show")),

    # Browser
    ([mod], "n", lazy.spawn("brave")),

    # Visual Code
    ([mod], "v", lazy.spawn("code-oss")),

    # File Manager
    ([mod], "e", lazy.spawn("nemo")),

    # Terminal
    ([mod], "t", lazy.spawn("alacritty")),

    # ------------ Hardware Configs ------------

    # Volume
    ([], "XF86AudioLowerVolume", lazy.spawn(
        "pactl set-sink-volume @DEFAULT_SINK@ -5%"
    )),
    ([], "XF86AudioRaiseVolume", lazy.spawn(
        "pactl set-sink-volume @DEFAULT_SINK@ +5%"
    )),
    ([], "XF86AudioMute", lazy.spawn(
        "pactl set-sink-mute @DEFAULT_SINK@ toggle"
    )),

    # Brightness
    ([], "XF86MonBrightnessUp", lazy.spawn("brightnessctl set +10%")),
    ([], "XF86MonBrightnessDown", lazy.spawn("brightnessctl set 10%-")),
]]


# GROUPS

groups = [
            Group("TERM", label="", spawn=["alacritty"]*3),
            Group("DEV", label=""),
            Group("NET", label="爵"),
            Group("FS", label=""),
            Group("SOCIAL", spawn=["station", "discord"], label=""),
            Group("MAIL", spawn=["mailspring"], label=""),
            Group("MEDIA", spawn=["spotify"], label="")
        ]

for i, group in enumerate(groups):
    # Each workspace is identified by a number starting at 1
    actual_key = str(i + 1)
    keys.extend([
        # Switch to workspace N (actual_key)
        Key([mod], actual_key, lazy.group[group.name].toscreen()),
        # Send window to workspace N (actual_key)
        Key([mod, "shift"], actual_key, lazy.window.togroup(group.name))
    ])


# LAYOUTS

layout_conf = {
    'border_focus': colors['magenta'][0],
    'border_width': 1,
    'margin': 4
}

layouts = [
    layout.MonadTall(**layout_conf),
    layout.Matrix(columns=2, **layout_conf),
    # layout.Bsp(),
    # layout.Columns(),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
    layout.Max(),
]


# WIDGETS

# Reusable configs for displaying different widgets on different screens

def base(fg='light', bg='dark'):
    return {
        'foreground': colors[fg],
        'background': colors[bg],
        'font': font
    }


separator = {
    'linewidth': 0,
    'padding': 5,
}

special_separator = {
    **base(),
    **separator
}

group_box = {
    **base(),
    'fontsize': 20,
    'margin_y': 5,
    'margin_x': 0,
    'padding_y': 8,
    'padding_x': 5,
    'borderwidth': 1,
    'active': colors['light'],
    'inactive': colors['light'],
    'rounded': False,
    'highlight_method': 'block',
    'this_current_screen_border': colors['blue'],
    'this_screen_border': colors['grey'],
    'other_current_screen_border': colors['dark'],
    'other_screen_border': colors['dark']
}

window_name = {
    **base(fg='blue'),
    'fontsize': 12,
    'padding': 5
}

systray = {
    'padding': 5
}

text_box = {
    'fontsize': 15,
    'padding': 5
}

powerline_sep = {
    "text": u'\ue0b2',
    "fontsize": 30,
    "padding": 0
}

pacman = {
    'execute': 'alacritty',
    'update_interval': 1800
}

net = {
    'interface': 'enp34s0',
    'format': '{down} ↓↑ {up}'
}

current_layout_icon = {
    'scale': 0.65
}

current_layout = {
    'padding': 5
}

clock = {
    'format': '%d/%m/%Y - %H:%M '
}


def workspaces():
    return [
        widget.Sep(**special_separator),
        widget.GroupBox(**group_box),
        widget.Sep(**special_separator),
        widget.WindowName(**window_name)
    ]


def powerline_base():
    return [
        widget.CurrentLayoutIcon(
            **base(bg='blue'),
            **current_layout_icon
        ),
        widget.CurrentLayout(
            **base(bg='blue'),
            **current_layout
        ),
        widget.TextBox(
            **base(fg='cyan', bg='blue'),
            **powerline_sep
        ),
        widget.TextBox(
            **base(bg='cyan'),
            fontsize=20,
            text=""
        ),
        widget.Clock(
            **base(bg='cyan'),
            **clock
        )
    ]


laptop_widgets = [
    *workspaces(),
    widget.Sep(
        **special_separator
    ),
    widget.Systray(
        **base(bg='dark'),
        **systray
    ),
    widget.Sep(
        **special_separator
    ),
    widget.TextBox(
        **base(bg='dark', fg='red'),
        **powerline_sep
    ),
    widget.TextBox(
        **base(bg='red'),
        fontsize=20,
        text='ﮮ'
    ),
    widget.Pacman(
        **base(bg='red'),
        **pacman
    ),
    widget.TextBox(
        **base(fg='violet', bg='red'),
        **powerline_sep
    ),
    widget.TextBox(
       **base(bg='violet'),
       fontsize=20,
       text=''
    ),
    widget.Net(
        **base(bg='violet'),
        **net
    ),
    widget.TextBox(
        **base(bg='violet', fg='blue'),
        **powerline_sep
    ),
    *powerline_base()
 ]


monitor_widgets = [
    *workspaces(),
    widget.TextBox(
        **base(fg='red', bg='dark'),
        **powerline_sep
    ),
    widget.TextBox(
       **base(bg='red'),
       fontsize=20,
       text=''
    ),
    widget.MemoryGraph(
        **base(bg='red'),
        graph_color=only_color("light"),
        border_color=only_color("light"),
        fill_color=only_color("light")+".3",
        type="line"

    ),
    widget.TextBox(
       **base(bg='red'),
       fontsize=20,
       text='﬙'
    ),
    widget.CPUGraph(
        **base(bg='red'),
        graph_color=only_color("light"),
        border_color=only_color("light"),
        fill_color=only_color("light")+".3",
        type="line"

    ),
    widget.TextBox(
        **base(fg='violet', bg='red'),
        **powerline_sep
    ),
    widget.TextBox(
       **base(bg='violet'),
       fontsize=20,
       text='墳'
    ),
    widget.Volume(
        **base(bg='violet'),
        step=1
    ),
    # widget.TextBox(
    #    **base(bg='orange'),
    #    fontsize=20,
    #    text=''
    # ),
    # widget.DF(
    #     **base(bg='orange'),
    #     measure='G',
    #     visible_on_warn=False,
    #     partition='/',
    #     format='/ ({uf}{m}|{r:.0f}%) - '
    # ),
    # widget.DF(
    #     **base(bg='orange'),
    #     measure='G',
    #     visible_on_warn=False,
    #     partition='/home',
    #     format='/home ({uf}{m}|{r:.0f}%)'
    # ),
    widget.TextBox(
        **base(bg='violet', fg='blue'),
        **powerline_sep
    ),
    *powerline_base()
]

widget_defaults = {
    'fontsize': 13,
    'padding': 2
}
extension_defaults = widget_defaults.copy()


# SCREENS

screens = [
    Screen(top=bar.Bar(monitor_widgets, 24, opacity=0.95), ),
    Screen(top=bar.Bar(laptop_widgets, 24, opacity=0.95))
]

# MOUSE

mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
        start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
        start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]


# OTHER STUFF

dgroups_key_binder = None
dgroups_app_rules = []  # type: List
main = None
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        {'wmclass': 'confirm'},
        {'wmclass': 'dialog'},
        {'wmclass': 'download'},
        {'wmclass': 'error'},
        {'wmclass': 'file_progress'},
        {'wmclass': 'notification'},
        {'wmclass': 'splash'},
        {'wmclass': 'toolbar'},
        {'wmclass': 'confirmreset'},  # gitk
        {'wmclass': 'makebranch'},  # gitk
        {'wmclass': 'maketag'},  # gitk
        {'wname': 'branchdialog'},  # gitk
        {'wname': 'pinentry'},  # GPG key password entry
        {'wmclass': 'ssh-askpass'},  # ssh-askpass
    ],
    border_focus=colors["green"][0]
)
auto_fullscreen = True
focus_on_window_activation = "smart"

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's lightlist.
wmname = "LG3D"
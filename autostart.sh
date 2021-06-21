#!/bin/sh

~/.config/qtile/scripts/compton-toggle.sh
dropbox 2> /dev/null >> /dev/null &
budgie-polkit-dialog &
feh -z --bg-fill .config/bg &
xsettingsd &
/usr/bin/xscreensaver --no-splash &

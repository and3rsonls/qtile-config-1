if pgrep -x "picom" > /dev/null
then
  killall picom
fi

picom -b --config ~/.config/qtile/scripts/compton.conf


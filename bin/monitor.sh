#!/bin/bash

# This script assumes the following:
# - Internal monitor with resolution 1920x1080 called eDP-1
# - External monitor with resolution 3200x2400 called HDMI-1
#   (In my setup this is a color e-ink: Dasung Paperlike 13K color)

# Alternative external monitor
# - External monitor with resolution 2200x1650 called HDMI-1
#   (In my setup this is a B/W e-ink: Dasung Paperlike 13K)


# I am running KDE 5, and I can't get it to handle this monitor setup well. Suggestions to use
# .xprofile is of no use since KDE overwrites these changes on startup. The best solution I have
# found so far is to use this script and use it to configure my monitors using xrandr.

# Check if exactly one parameter is provided
if [ $# -ne 1 ]; then
    echo "Error: Please provide exactly one parameter. Valid values:"
    echo "  \"laptop\", \"laptop+eink\", \"eink\""
    exit 1
fi

SETUP="$1"

# Execute different xrandr commands based on the parameter
case "$SETUP" in
    "laptop+eink")
        echo "Setting up laptop + eink"
        # fb is set high enough to have space for both scaled monitor screens (1600 + 2304 = 3904 < 4000)
        # Using left-of does not work, since it tries to use the unscaled position which causes a "gap" between the screens.
        set -x
        /usr/bin/xrandr --output HDMI-1 --mode 3200x2400 --scale 0.5x0.5 --pos 0x0 --output eDP-1 --mode 1920x1080 --scale 1.2x1.2 --pos 1600x0 --fb 4000x2400
        # /usr/bin/xrandr --output HDMI-1 --mode 2200x1650 --scale 0.8x0.8 --pos 0x0 --output eDP-1 --mode 1920x1080 --scale 1.2x1.2 --pos 1760x0 --fb 4000x2400
        set +x
       ;;
    "laptop")
        echo "Setting up laptop only"
        set -x
        /usr/bin/xrandr --output HDMI-1 --off --output eDP-1 --mode 1920x1080 --scale 1.2x1.2 --pos 1600x0 --fb 4000x2400        
        set +x
        ;;
    "eink")
        echo "Setting up eink only"
        set -x
        /usr/bin/xrandr --output HDMI-1 --mode 3200x2400 --scale 0.5x0.5 --pos 0x0 --output eDP-1 --off
        # /usr/bin/xrandr --output HDMI-1 --mode 2200x1650 --scale 0.5x0.5 --pos 0x0 --output eDP-1 --off
        set +x
        ;;
    *)
        echo "Error: Invalid parameter. Use 'laptop', 'laptop+eink', or 'eink'"
        exit 1
        ;;
esac

# Usually it is necessary to restart the plasmashell at this point, or the panel bugs out. This is
# not always the case, but it seem to happen always when both monitors are in use.
echo "Restarting plasmashell"
kquitapp5 plasmashell > /dev/null 2>&1 && rm -R ~/.cache/plasma* > /dev/null 2>&1 && kstart5 plasmashell > /dev/null 2>&1

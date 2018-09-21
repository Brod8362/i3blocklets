#!/bin/bash
# Copyright (C) 2014 Alexander Keller <github@nycroth.com>

#this is a modified version and not the original 
#------------------------------------------------------------------------

INTERFACE="wlp3s0"

#------------------------------------------------------------------------

# As per #36 -- It is transparent: e.g. if the machine has no battery or wireless
# connection (think desktop), the corresponding block should not be displayed.
#[[ ! -d /sys/class/net/${INTERFACE}/wireless ]] ||
#    [[ "$(cat /sys/class/net/$INTERFACE/operstate)" = 'down' ]] && exit

#------------------------------------------------------------------------

QUALITY=$(grep $INTERFACE /proc/net/wireless | awk '{ print int($3 * 100 / 70) }')
CONNECTED=$(cat /sys/class/net/$INTERFACE/carrier)
STATUS=$(nmcli r wifi)

#------------------------------------------------------------------------
#full, short

# Left click
if [[ "${BLOCK_BUTTON}" -eq 1 ]]; then
  nmcli r wifi on
# Middle click
elif [[ "${BLOCK_BUTTON}" -eq 2 ]]; then
  notify-send "WiFi: ${STATUS}"
# Right click
elif [[ "${BLOCK_BUTTON}" -eq 3 ]]; then
  nmcli r wifi off
fi


if [ $STATUS == "disabled" ]; then
    echo "WLAN Disabled"
    echo "WLAN Disabled"
    echo "#29292b"
    exit
fi


if [ -z $QUALITY ]; then
    echo "No Network"
    echo "No Network"
    echo "#FF0000"
    exit
fi

echo WLAN $QUALITY%
echo $QUALITY%
echo "#00FF00"

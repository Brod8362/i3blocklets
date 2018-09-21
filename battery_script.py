#!/usr/bin/env python3
#
# Copyright (C) 2016 James Murphy
# Licensed under the GPL version 2 only
#
# A battery indicator blocklet script for i3blocks

from subprocess import check_output
import os

status = check_output(['acpi'], universal_newlines=True)

if not status:
    # stands for no battery found
    fulltext = "<span color='red'><span font='FontAwesome'>\uf00d \uf240</span></span>"
    percentleft = 100
else:
    # if there is more than one battery in one laptop, the percentage left is 
    # available for each battery separately, although state and remaining 
    # time for overall block is shown in the status of the first battery 
    batteries = status.split("\n")
    state_batteries=[]
    commasplitstatus_batteries=[]
    percentleft_batteries=[]
    for battery in batteries:
        if battery!='':
            state_batteries.append(battery.split(": ")[1].split(", ")[0])
            commasplitstatus = battery.split(", ")
            percentleft_batteries.append(int(commasplitstatus[1].rstrip("%\n")))
            commasplitstatus_batteries.append(commasplitstatus)
    state = state_batteries[0]
    commasplitstatus = commasplitstatus_batteries[0]
    percentleft = int(sum(percentleft_batteries)/len(percentleft_batteries))
    # stands for charging
    FA_LIGHTNING = "<span color='yellow'><span font='FontAwesome'>\uf0e7</span></span>"

    # stands for plugged in
    FA_PLUG = "<span font='FontAwesome'>\uf1e6</span>"

    fulltext = ""
    timeleft = ""

    if state == "Discharging":
        time = commasplitstatus[-1].split()[0]
        time = ":".join(time.split(":")[0:2])
        timeleft = " ({})".format(time)
    elif state == "Full":
        fulltext = FA_PLUG + " "
    elif state == "Unknown":
        fulltext = "<span font='FontAwesome'>\uf128</span> "
    else:
        fulltext = FA_LIGHTNING + " " + FA_PLUG + " "
    def color(percent):
        batteryicon = "\uf240" #default icon
        if percent <= 10:
            # exit code 33 will turn background red
            # thank you for telling me previous programmer
            batteryicon = "\uf244"
            return "#FFFFFF", batteryicon
        if percent < 20:
            batteryicon = "\uf243"
            return "#FF3300", batteryicon
        if percent < 30:
            batteryicon = "\uf243"
            return "#FF6600", batteryicon
        if percent < 40:
            batteryicon = "\uf242"
            return "#FF9900", batteryicon
        if percent < 50:
            batteryicon = "\uf242"
            return "#FFCC00", batteryicon
        if percent < 60:
            batteryicon = "\uf241"
            return "#FFFF00", batteryicon
        if percent < 70:
            batteryicon = "\uf241"
            return "#FFFF33", batteryicon
        if percent < 80:
            batteryicon = "\uf241"
            return "#FFFF66", batteryicon
        return "#FFFFFF", batteryicon

    form =  '<span color="{}">'+color(percentleft)[1]+' {}%</span>'
    fulltext += form.format(color(percentleft)[0], percentleft)
    fulltext += timeleft


print(fulltext)
print(fulltext)
if percentleft <= 10:
    exit(33)

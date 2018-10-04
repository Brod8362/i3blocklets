#!/bin/bash


#connect vpn (left click)
if [[ "${BLOCK_BUTTON}" -eq 1 ]]; then
	sudo /usr/local/bin/connect_vpn
#kill vpn (right click)
elif [[ "${BLOCK_BUTTON}" -eq 3 ]]; then
	sudo /usr/local/bin/kill_vpn
fi

FILE=/sys/class/net/tun0/operstate

#this is the final output of the block
if [ -f $FILE ]; then
	IP=$(ip a |grep tun0 | grep -o "[0-9]*\.[0-9]*\.[0-9]*\.[0-9]*")
	echo "$IP"
	echo "up"
	echo "#00FF00"
else
	echo "down"
	echo "down"
	echo "#29292b"
fi

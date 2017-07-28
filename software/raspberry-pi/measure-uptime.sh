#!/bin/sh

# every minute, write the current uptime into a file

utfile=uptime.txt
delay_s=60

while true; do
	echo "updated $utfile"
	uptime > $utfile
	sleep $delay_s
done

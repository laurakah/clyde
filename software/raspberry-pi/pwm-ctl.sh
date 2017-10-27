#!/bin/bash

set -e
set -u
set -x

init_dirpin() {
	pin_no="$1"
	gpio_basedir="/sys/class/gpio/gpio${pin_no}"
	if [ ! -d $gpio_basedir ]; then
		echo $pin_no		> /sys/class/gpio/export
	fi
	echo out > $gpio_basedir/direction
	echo 0 > $gpio_basedir/value
}

init_pwm() {
	pwm_chip="$1"
	pwm_no="$2"
	pwm_period="$3"
	pwm_duty="$4"
	pwm_basedir="/sys/class/pwm/pwmchip${pwm_chip}"
	if [ ! -d $pwm_basedir/pwm${pwm_no} ]; then
		echo $pwm_no		> $pwm_basedir/export
	fi
	echo $pwm_period	> $pwm_basedir/pwm${pwm_no}/period
	echo $pwm_duty		> $pwm_basedir/pwm${pwm_no}/duty_cycle
	echo 1			> $pwm_basedir/pwm${pwm_no}/enable
}

init_motor0() {
	init_dirpin 16
	init_pwm 0 0 10000000 8000000
}

init_motor1() {
	init_dirpin 6
	init_pwm 0 1 10000000 8000000
}

main() {
	init_motor0
	init_motor1
}

main

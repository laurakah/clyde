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
	pwm_duty="$1"
	pwm_period="10000000" # 100 Hz in µHz
	init_dirpin 16
	init_pwm 0 0 $pwm_period $pwm_duty # 8000000
}

init_motor1() {
	pwm_duty="$1"
	pwm_period="10000000" # 100 Hz in µHz
	init_dirpin 6
	init_pwm 0 1 $pwm_period $pwm_duty # 8 000 000
}

main() {
	pwm_duty_percent="$1"
	pwm_duty="${1}00000"
	init_motor0 $pwm_duty
	init_motor1 $pwm_duty
}

main $@

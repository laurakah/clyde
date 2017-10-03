#!/usr/bin/python

import RPi.GPIO
import time

def read_switch(pin_no):
    return RPi.GPIO.input(pin_no)

def handle_event(pin_no):
    print "pin %d state = %d" % (pin_no, read_switch(pin_no))

def switches_setup():
	RPi.GPIO.setmode(RPi.GPIO.BOARD)
	# configure direction, pull-ups and
	# event handling
	for pin_no in [12, 16, 18, 22]:
                print "Setting up pin %d" % pin_no
		RPi.GPIO.setup(pin_no, RPi.GPIO.IN, RPi.GPIO.PUD_UP)
		RPi.GPIO.add_event_detect(pin_no, RPi.GPIO.BOTH)
                RPi.GPIO.add_event_callback(pin_no, handle_event)
def main():
        print "Setting up switches ..."
        switches_setup()
        print "Starting idle loop ..."
        while True:
            time.sleep(1)

if __name__ == '__main__':
        main()

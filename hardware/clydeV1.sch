EESchema Schematic File Version 2
LIBS:power
LIBS:device
LIBS:transistors
LIBS:conn
LIBS:linear
LIBS:regul
LIBS:74xx
LIBS:cmos4000
LIBS:adc-dac
LIBS:memory
LIBS:xilinx
LIBS:microcontrollers
LIBS:dsp
LIBS:microchip
LIBS:analog_switches
LIBS:motorola
LIBS:texas
LIBS:intel
LIBS:audio
LIBS:interface
LIBS:digital-audio
LIBS:philips
LIBS:display
LIBS:cypress
LIBS:siliconi
LIBS:opto
LIBS:atmel
LIBS:contrib
LIBS:valves
LIBS:clydeV1-cache
EELAYER 25 0
EELAYER END
$Descr A4 11693 8268
encoding utf-8
Sheet 1 1
Title ""
Date ""
Rev ""
Comp ""
Comment1 ""
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
$Comp
L CONN_02X20 J2
U 1 1 59997E0D
P 5100 3850
F 0 "J2" H 5100 4900 50  0000 C CNN
F 1 "RPIZEROW" V 5100 3850 50  0000 C CNN
F 2 "Socket_Strips:Socket_Strip_Straight_2x20_Pitch2.54mm" H 5100 2900 50  0001 C CNN
F 3 "" H 5100 2900 50  0001 C CNN
	1    5100 3850
	1    0    0    1   
$EndComp
Wire Wire Line
	6650 4600 5350 4600
Text Label 5550 4600 0    60   ~ 0
GND
Wire Wire Line
	5350 4500 5550 4500
Text Label 5550 4500 0    60   ~ 0
GPIO14/TXD
Wire Wire Line
	5350 4400 5550 4400
Text Label 5550 4400 0    60   ~ 0
GPIO15/RXD
$Comp
L CONN_01X03_MALE J1
U 1 1 59997F6D
P 1800 1700
F 0 "J1" H 1800 1975 50  0000 C CNN
F 1 "UART" H 1825 1425 50  0000 C CNN
F 2 "Pin_Headers:Pin_Header_Angled_1x03_Pitch2.54mm" H 1800 1900 50  0001 C CNN
F 3 "" H 1800 1900 50  0001 C CNN
	1    1800 1700
	1    0    0    -1  
$EndComp
Wire Wire Line
	2100 1900 2250 1900
Wire Wire Line
	2100 1700 2250 1700
Wire Wire Line
	2100 1500 2250 1500
Text Label 2250 1500 0    60   ~ 0
GND
Text Label 2250 1700 0    60   ~ 0
GPIO14/TXD
Text Label 2250 1900 0    60   ~ 0
GPIO15/RXD
$Comp
L CONN_02X03 J4
U 1 1 599980F6
P 8200 3400
F 0 "J4" H 8200 3600 50  0000 C CNN
F 1 "MDRV" H 8200 3200 50  0000 C CNN
F 2 "Pin_Headers:Pin_Header_Angled_2x03_Pitch2.54mm" H 8200 2200 50  0001 C CNN
F 3 "" H 8200 2200 50  0001 C CNN
	1    8200 3400
	1    0    0    1   
$EndComp
$Comp
L CONN_02X04 J3
U 1 1 5999816B
P 8250 4600
F 0 "J3" H 8250 4850 50  0000 C CNN
F 1 "COLL_SW" H 8250 4350 50  0000 C CNN
F 2 "Pin_Headers:Pin_Header_Angled_2x04_Pitch2.54mm" H 8250 3400 50  0001 C CNN
F 3 "" H 8250 3400 50  0001 C CNN
	1    8250 4600
	1    0    0    -1  
$EndComp
Wire Wire Line
	5350 4300 5550 4300
Wire Wire Line
	5350 4100 5550 4100
Wire Wire Line
	5350 4000 5550 4000
Wire Wire Line
	5350 3800 5550 3800
Text Label 5550 4300 0    60   ~ 0
GPIO18
Text Label 5550 4100 0    60   ~ 0
GPIO23
Text Label 5550 4000 0    60   ~ 0
GPIO24
Text Label 5550 3800 0    60   ~ 0
GPIO25
Wire Wire Line
	5350 3900 6650 3900
Text Label 5550 3900 0    60   ~ 0
GND
Wire Wire Line
	8000 4750 7850 4750
Wire Wire Line
	8000 4650 7850 4650
Wire Wire Line
	8000 4550 7850 4550
Wire Wire Line
	8000 4450 7850 4450
Text Label 7850 4750 2    60   ~ 0
GPIO18
Text Label 7850 4650 2    60   ~ 0
GPIO23
Text Label 7850 4550 2    60   ~ 0
GPIO24
Text Label 7850 4450 2    60   ~ 0
GPIO25
Wire Wire Line
	8500 4450 8600 4450
Wire Wire Line
	8500 4550 8600 4550
Wire Wire Line
	8600 4650 8500 4650
Wire Wire Line
	8500 4750 8700 4750
Wire Wire Line
	8600 4450 8600 4750
Connection ~ 8600 4550
Connection ~ 8600 4750
Connection ~ 8600 4650
Text Label 8700 4750 0    60   ~ 0
GND
Wire Wire Line
	4850 3300 4650 3300
Wire Wire Line
	4850 3200 4650 3200
Wire Wire Line
	5350 3300 5550 3300
Wire Wire Line
	5350 3200 6650 3200
Wire Wire Line
	5350 3100 5550 3100
Text Label 5550 3200 0    60   ~ 0
GND
Text Label 5550 3300 0    60   ~ 0
GPIO12/PWM0/M1OUT
Text Label 4650 3200 2    60   ~ 0
GPIO13/PWM1/M2OUT
Text Label 4650 3300 2    60   ~ 0
GPIO6/M2DIR
Text Label 5550 3100 0    60   ~ 0
GPIO16/M1DIR
Wire Wire Line
	7950 3300 7850 3300
Wire Wire Line
	7950 3400 7850 3400
Wire Wire Line
	7950 3500 7850 3500
Wire Wire Line
	8450 3300 8550 3300
Wire Wire Line
	8450 3400 8550 3400
Wire Wire Line
	8450 3500 8550 3500
Text Label 7850 3500 2    60   ~ 0
GND
Text Label 7850 3400 2    60   ~ 0
GPIO12/PWM0/M1OUT
Text Label 7850 3300 2    60   ~ 0
GPIO13/PWM1/M2OUT
Text Label 8550 3300 0    60   ~ 0
GPIO6/M2DIR
Text Label 8550 3400 0    60   ~ 0
GPIO16/M1DIR
Text Label 8550 3500 0    60   ~ 0
5V
Wire Wire Line
	5350 4700 5550 4700
Text Label 5550 4700 0    60   ~ 0
5V
Wire Wire Line
	6650 3200 6650 4600
Connection ~ 6650 3900
$EndSCHEMATC

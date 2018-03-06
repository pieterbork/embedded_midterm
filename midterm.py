#!/usr/bin/python
import mraa
from time import sleep,time
from Servo import *
from urllib import urlencode
from urllib2 import urlopen


sound = mraa.Aio(5)
button = mraa.Gpio(8)
pigtail = mraa.Gpio(10)
servo = Servo("servo")
servo.attach(3)
servo.write(0)
button.dir(mraa.DIR_IN)
led_yellow = mraa.Gpio(2)
led_blue = mraa.Gpio(11)
led_red = mraa.Gpio(4)
led_green = mraa.Gpio(5)
led_flasm1 = mraa.Gpio(6)
led_flasm2 = mraa.Gpio(7)
pigtail.dir(mraa.DIR_OUT)
led_yellow.dir(mraa.DIR_OUT)
led_blue.dir(mraa.DIR_OUT)
led_red.dir(mraa.DIR_OUT)
led_green.dir(mraa.DIR_OUT)
led_flasm1.dir(mraa.DIR_OUT)
led_flasm2.dir(mraa.DIR_OUT)


#Configurable Variables
pulse_min = 0.01
pulse_max = 0.2
read_delay = 0.05
num_readings_list = 20
timeout = 500
pulse_time_dif_min = 0.15
pulse_time_dif_max = 0.65
peak_threshold = 1.5


#Global Variables
last_pulse_time = 0
pigtail_on = False

readings_list = []
for i in range(0, num_readings_list):
    readings_list.append(10000)
last_level = 0 


def clear_leds():
    led_yellow.write(0) 
    led_blue.write(0) 
    led_red.write(0) 
    led_green.write(0) 
    led_flasm1.write(0) 
    led_flasm2.write(0) 

def readSound():
    reading = sound.read()
    reading = reading * .5
    readings_list.append(reading)
    readings_list.pop(0)
#    print(readings_list, sum(readings_list))
    last_level = sum(readings_list)
    led_sound_meter(readings_list, reading)
    return reading

def led_sound_meter(readings_list, sound_level):
    clear_leds()
    avg = (sum(readings_list)/len(readings_list))
    dev = avg * 0.1
    if (sound_level > (avg - (3 * dev))):
        led_yellow.write(1)
    if (sound_level > (avg - (1.5 * dev))):
        led_blue.write(1)
    if (sound_level > avg):
        led_red.write(1)
    if (sound_level > (avg + (0.5 * dev))):
        led_green.write(1)
    if (sound_level > (avg + (1.5 * dev))):
        led_flasm1.write(1)
    if (sound_level > (avg * peak_threshold)):
        led_flasm2.write(1)

def readPulse():
    pulse_time = 0
    clap_threshold = (sum(readings_list)/len(readings_list)) * peak_threshold
    if (readSound() >= clap_threshold):
        print("Pulse detected")
        pulse_time = time()
        while (readSound() >= clap_threshold and (time() - pulse_time < timeout)):
#            clap_threshold = (sum(readings_list)/len(readings_list)) * 1.25
            sleep(read_delay)
        pulse_time = time() - pulse_time
        print("Pulse length: " + str(pulse_time))
    return pulse_time

def toggle_disco_party(pigtail_is_on):
    url = "http://192.168.20.231"
    data = {}
    if pigtail_is_on:
        pigtail.write(0)
        servo.write(0)
        pigtail_is_on = False
        data = {'pwr': "off"}
    else:
        pigtail.write(1)
        servo.write(180)
        pigtail_is_on = True
        data = {'pwr': "on"}
    try:
        content = urlopen(url=url, data=data)
        print("Post successful!")
    except:
        pass
    return pigtail_is_on

while(not(button.read())):
    pulse_length = readPulse()
    if ( pulse_length >= pulse_min and pulse_length <= pulse_max ):
        pulse_time = time()
        time_dif = pulse_time - last_pulse_time
        print("Time diff: " + str(time_dif))
        if (time_dif >= pulse_time_dif_min and time_dif <= pulse_time_dif_max):
            print("###############\nCLAP DETECTED!\n###############")
            pigtail_on = toggle_disco_party(pigtail_on)
            last_pulse_time = 0
        else:
            last_pulse_time = pulse_time;
    sleep(read_delay)

clear_leds()
pigtail.write(0)
servo.write(0)

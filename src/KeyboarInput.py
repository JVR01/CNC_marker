#!/usr/bin/env python
import rospy
import re

import drivers
from time import sleep


#neoPixel LED https://github.com/rpi-ws281x/rpi-ws281x-python
import time
from rpi_ws281x import PixelStrip, Color
import argparse
# LED strip configuration:
LED_COUNT = 1        # Number of LED pixels.
LED_PIN = 18       # GPIO pin connected to the pixels (18 uses PWM!).
# LED_PIN = 10        # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10          # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255  # Set to 0 for darkest and 255 for brightest
LED_INVERT = False    # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)


from evdev import InputDevice, categorize, ecodes
from std_msgs.msg import String

import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)

led = 14
switch_start = 24 #Blue18 Yell24  RED23
LED_GREEN = 20

GPIO.setup(led, GPIO.OUT)
GPIO.setup(LED_GREEN, GPIO.OUT)
GPIO.setup(switch_start, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Set pin   GPIO.PUD_DOWN-con3.3v    GPIO.PUD_UP-conGRD

dev = InputDevice('/dev/input/event0')
display = drivers.Lcd()
keyboard_input = "awesome"
Counter = 0
prev_inp1 = 1

print('test')
print(dev)


def callback(data):
    global prev_inp1
    rospy.loginfo(rospy.get_caller_id() + " I heard: %s", data.data)
    blink(LED_GREEN)
    blink_rgb(1,0,1)
    prev_inp1 = 1

    
    
def listener():
    rospy.init_node('raspi_node', anonymous=True)
    rospy.Subscriber("chatter", String, callback)
    #rospy.spin() 
    
def talker():
    global keyboard_input
    global prev_inp1
    #rospy.init_node('talker', anonymous=True)
    #rate = rospy.Rate(10) # 10hz
    #while not rospy.is_shutdown():
    pub = rospy.Publisher('Keyboard_Input', String, queue_size=10)
    #keyboard_input = "hello world %s" % rospy.get_time()
    rospy.loginfo(keyboard_input)
    pub.publish(keyboard_input)
    #rate.sleep()       
'''
for event in dev.read_loop():
    if event.type == ecodes.EV_KEY:
        print(categorize(event))
'''
def colorWipe(strip, color, wait_ms=50):
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms / 1000.0)

def show_screen(word):
    display.lcd_clear()
    #print("Writing to display")
    display.lcd_display_string(keyboard_input,1)
    display.lcd_display_string(word, 2) # Write line of text to second line of display
    #sleep(2)                                           # Give time for the message to be read
    #display.lcd_display_string("I am a display!", 1)   # Refresh the first line of display with a different message
    #sleep(2)                                           # Give time for the message to be read
    # Clear the display of any data     

def toggle_led():
    channel_is_on = GPIO.input(led)
    print('Switch_start status = ', GPIO.input(switch_start))
    print('LED status = ', channel_is_on)

    if channel_is_on:
        print('device off')
        GPIO.output(led, GPIO.LOW)
        time.sleep(0.2)
    else:
        print('device on')
        GPIO.output(led, GPIO.HIGH)
        time.sleep(0.2)
    

def helper(dev):
    global keyboard_input
    print('------------------------------------')
    for ev in dev.read_loop():
        
        if ev.type == ecodes.EV_KEY:
            key_data= categorize(ev)
            print(key_data.keycode)
            #print(key_data)
               
            if key_data.keystate and key_data.keycode == 'KEY_1':
                print('toggle')
                toggle_led()
                blink_rgb(0,0,1)#blue
            elif key_data.keystate and key_data.keycode == 'KEY_ESC': 
                print('I get out of here!')
                blink(led)
                blink_rgb(1,0,0)#red
                return
            elif key_data.keystate and key_data.keycode == 'KEY_BACKSPACE': 
                print('erase routine***************')
                msglen = len(keyboard_input) #// 2
                #text = 'abcdefg'
                #text = text[:1] + 'Z' + text[2:]
                keyboard_input = keyboard_input[:msglen-1]
                print('size of msg: ' , msglen)
                print ("recorted msg: " + keyboard_input)
                
            elif key_data.keystate and key_data.keycode == 'KEY_SPACE': 
                
                keyboard_input = keyboard_input + ' '
                   
                
            elif key_data.keystate:
                print('------------------------------------')
                m = re.search('(?<=_)\w+', key_data.keycode)
                if  m:
                    found = m.group(0)
                    print(found)
                    keyboard_input = keyboard_input + found
                    #pass 
            show_screen("nix")    
                
def Interrupt_Start(channel):
  global Counter
  global prev_inp1
  inp = GPIO.input(switch_start)

  if (not inp): #prev_inp1 == 1
     # Counter um eins erhoehen und ausgeben
     Counter = Counter + 1
     print ("Counter: " + str(Counter))
     talker() 
     blink(LED_GREEN)
     blink_rgb(0, 1, 0) #r,g,b
     prev_inp1 = 0

     
          
def blink(led_pin):
    
    for i in range(3):
        GPIO.output(led_pin, GPIO.LOW)
        time.sleep(0.08)
        GPIO.output(led_pin, GPIO.HIGH)
        time.sleep(0.08)

def blink_rgb(r , g , b):
    print('Color wipe animations.')
    #colorWipe(strip, Color(255, 0, 0))  # Red wipe
    #colorWipe(strip, Color(0, 255, 0))  # Green wipe
    #colorWipe(strip, Color(0, 0, 255))  # Blue wipe
    for i in range(3):
        colorWipe(strip, Color(255*r, 255*g, 255*b))  # Red wipe
        time.sleep(0.08)
        colorWipe(strip, Color(0, 0, 0))
        time.sleep(0.08)        

GPIO.add_event_detect(switch_start, GPIO.RISING, callback = Interrupt_Start, bouncetime = 500)  
        
if __name__ == '__main__':
    try:
       print("was du labberst!!??")
       strip.begin() # init the led
       listener()
       helper(dev)
    except KeyboardInterrupt: # If CTRL+C is pressed, exit cleanly:
       print("Keyboard interrupt")   
    except rospy.ROSInterruptException:
        pass
    except:
       print("some error") 
    finally:
       print("clean up") 
       GPIO.cleanup() # cleanup all GPIO
       display.lcd_clear()


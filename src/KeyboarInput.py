#!/usr/bin/env python3

'''
this script Takes and procces the Keyboard inputs and also controls the LCD-screen and the rgb-LED
the given text ist Published throgh the topic: 'Keyboard_Input' 

'''
from turtle import delay
import rospy
import re
import os
import drivers
from time import sleep
#>>>>>import commands
import subprocess

#neoPixel LED https://github.com/rpi-ws281x/rpi-ws281x-python
import time
from rpi_ws281x import PixelStrip, Color
import argparse

import rosgraph
import socket

# LED strip configuration:
LED_COUNT = 1        # Number of LED pixels.
LED_PIN = 18       # GPIO pin connected to the pixels (18 uses PWM!).s
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

#led = 14
switch_start = 24 #Yellow
switch_stop = 23 #Red
switch_clear = 25#Blue
#LED_GREEN = 20

#GPIO.setup(led, GPIO.OUT)
#GPIO.setup(LED_GREEN, GPIO.OUT)
GPIO.setup(switch_start, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Set pin   GPIO.PUD_DOWN-con3.3v    GPIO.PUD_UP-conGRD
GPIO.setup(switch_stop, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(switch_clear, GPIO.IN, pull_up_down=GPIO.PUD_UP)

dev = InputDevice('/dev/input/event0')
display = drivers.Lcd()
keyboard_input = ""
status = "Starting..."
Counter = 0
prev_inp1 = 1


print('test')
print(dev)
print(dev.name)

if (dev.name != "2.4G Composite Devic"):
    print("Defaul keyboard failed but trying alternative ...")
    dev = InputDevice('/dev/input/event1')                         #     ('/dev/input/event3'))      Does this always work? nooo! TODO
    print(dev)
    print(dev.name)


def callback_status(data): #"status" topic
    global Counter
    global status
    rospy.loginfo(rospy.get_caller_id() + " I heard: %s", data.data)
    status = data.data
    Counter = Counter + 1
    print ("Counter: " + str(Counter))
    #show_screen(status + ":" + str(Counter)) 
    show_screen(status) 
    
    
def listener():
    rospy.init_node('raspi_node', anonymous=True)
    #rospy.Subscriber("chatter", String, callback)
    rospy.Subscriber("status", String, callback_status)
    #rospy.spin()
    # Set rospy to exectute a shutdown function when terminating the script
    rospy.on_shutdown(myhook)

    
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

def colorWipe(strip, color, wait_ms=50):
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms / 1000.0)

def show_screen(word):
    global keyboard_input
    display.lcd_clear()
    display.lcd_display_string(keyboard_input,1)
    display.lcd_display_string(word, 2) # Write line of text to second line of display    

def keyboard_read_helper(dev):
    global keyboard_input
    global status

    print('------------------keyboard_read_helper started------------------')
    for ev in dev.read_loop():
        
        #print('...Into keyRead loop!')
        try:
            rosgraph.Master('/rostopic').getPid()
        except socket.error:
            print('Finishing the keyRead loop!')
            exit()
             

        if ev.type == ecodes.EV_KEY:
            key_data= categorize(ev)
            print(key_data.keycode)

            if key_data.keystate == key_data.key_down:
                c = key_data.keycode
                print('c: ' , c)
                #print(categorize(ev))
                #print(key_data)
               
                if key_data.keystate and key_data.keycode == 'KEY_F1':
                    print('toggle')
                    #toggle_led()
                    blink_rgb(0,0,1)#blue
                elif key_data.keystate and key_data.keycode == 'KEY_ESC': 
                    print('I get out of here!')
                    show_screen("Leaving..")
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
                    print('----------------key state--------------------')
                    m = re.search('(?<=_)\w+', key_data.keycode)
                    if  m:
                        found = m.group(0)
                        print(found)
                        keyboard_input = keyboard_input + found
                        #pass 
                status = "Texting..."
                print("writting to screen")        
                show_screen(status)
                time.sleep(500.0 / 1000.0) #'test' 

        #print("made it here------")
    print("out of the key_read_loop------") 
                
def Interrupt_Start(channel): #Yellow button Pressed -->send word....engrave!
  global Counter
  global prev_inp1
  inp = GPIO.input(switch_start)

  if (not inp):
     show_screen("Sending...")
     show_screen("Sending...")
     talker() 
     blink_rgb(1, 1, 0) #r,g,b Yellow
     prev_inp1 = 0

def Interrupt_Clear(channel):  #Blue button Pressed--> clear Screen and Text and let me start again!
  global Counter
  global keyboard_input
  print ("BLUE button printed..." )
  inp = GPIO.input(switch_clear)

  if (not inp): #prev_inp1 == 1
     # Counter um eins erhoehen und ausgeben
     Counter = 0
     display = drivers.Lcd()
     print ("Clear..." ) 
     blink_rgb(0 , 0, 1) #r,g,b 
     keyboard_input = ""
     show_screen("Clear...")
     show_screen("Clear...")
     wrong_div = 24/(8-8)
     
     
         
def Interrupt_Stop(channel): #Red button Pressed--> restart the machine!
  
  inp = GPIO.input(switch_stop)

  if (not inp): #prev_inp1 == 1
     # Counter um eins erhoehen und ausgeben
     show_screen("STOP...")
     show_screen("STOP...")
     blink_rgb(1 , 0, 0) #r,g,b
     # Command to execute
     os.system("sudo systemctl restart cnc.service")
     #os.system("sudo reboot")
     blink_rgb(1 , 1, 1) #r,g,b
     print(os.getpid())

     #++os.system("sudo bash /home/tamer/ros_catkin_ws/src/CNC_marker/src/stop_start.sh >>erase.txt")

def blink_rgb(r , g , b):
    #print('Color wipe animations.')
    #colorWipe(strip, Color(255, 0, 0))  # Red wipe
    #colorWipe(strip, Color(0, 255, 0))  # Green wipe
    #colorWipe(strip, Color(0, 0, 255))  # Blue wipe
    for i in range(3):
        colorWipe(strip, Color(255*r, 255*g, 255*b))  # Red wipe
        time.sleep(0.08)
        colorWipe(strip, Color(0, 0, 0))
        time.sleep(0.08)

def start_topic():
    global keyboard_input
    
    keyboard_input = "init"
    
    for i in range(2):
        talker()
        time.sleep(0.2)
        
    keyboard_input = ""   

def except_hook(type, value, tback):
    # manage unhandled exception here
    print("unmanaged exeception**************") 
    os.sys.__excepthook__(type, value, tback) # then call the default handler

def myhook():
    print ("Shutdown time!")
            

GPIO.add_event_detect(switch_start, GPIO.FALLING, callback = Interrupt_Start, bouncetime = 250)  
GPIO.add_event_detect(switch_stop, GPIO.FALLING, callback = Interrupt_Stop, bouncetime = 250) 
GPIO.add_event_detect(switch_clear, GPIO.FALLING, callback = Interrupt_Clear, bouncetime = 250) 

os.sys.excepthook = except_hook
        
if __name__ == '__main__':
    try:
       print("Executing main")
       strip.begin() # init the RGB-led
       show_screen(status)
       blink_rgb(0,1,0)#rgb
       listener()
       start_topic()
       keyboard_read_helper(dev)
    except KeyboardInterrupt: # If CTRL+C is pressed, exit cleanly:
       print("Keyboard interrupt")   
    except rospy.ROSInterruptException:
        pass
        print("MIO rospi error some error")
    except:
       print("some error") 
    finally:
       print("clean up") 
       GPIO.cleanup() # cleanup all GPIO
       display.lcd_clear()

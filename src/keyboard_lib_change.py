#!/usr/bin/env python3

'''
This script processes keyboard inputs, controls an LCD screen and RGB LED,
and publishes text through the 'Keyboard_Input' topic
'''

import rospy
import rosnode
import re
import os
import sys
import threading
import gpiod
import drivers
from time import sleep
import subprocess

# NeoPixel LED setup
from rpi_ws281x import PixelStrip, Color
import time

import rosgraph
import socket

# LED strip configuration:
LED_COUNT = 1        # Number of LED pixels
LED_PIN = 18         # GPIO pin connected to the pixels (18 uses PWM!)
LED_FREQ_HZ = 800000 # LED signal frequency in hertz
LED_DMA = 10         # DMA channel to use for generating signal
LED_BRIGHTNESS = 255 # Set to 0 for darkest and 255 for brightest
LED_INVERT = False   # True to invert the signal
LED_CHANNEL = 0      # set to '1' for GPIOs 13, 19, 41, 45 or 53

strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)

from evdev import InputDevice, categorize, ecodes
from std_msgs.msg import String

# GPIO Configuration
GPIO_CHIP = 'gpiochip0'
switch_start = 24  # Yellow button (BCM 24)
switch_stop = 23   # Red button (BCM 23)
switch_clear = 25  # Blue button (BCM 25)

# Initialize GPIO
try:
    chip = gpiod.Chip(GPIO_CHIP)
    
    # Get GPIO lines
    start_line = chip.get_line(switch_start)
    stop_line = chip.get_line(switch_stop)
    clear_line = chip.get_line(switch_clear)
    
    # Try to configure with pull-ups (new API)
    try:
        config = gpiod.line_request()
        config.consumer = "buttons"
        config.request_type = gpiod.line_request.DIRECTION_INPUT
        try:
            config.flags = gpiod.line_request.FLAG_BIAS_PULL_UP
        except AttributeError:
            print("Software pull-up not supported, using hardware pull-ups")
        
        start_line.request(config)
        stop_line.request(config)
        clear_line.request(config)
    except AttributeError:
        # Fallback for older API
        start_line.request(consumer="buttons", type=gpiod.LINE_REQ_DIR_IN)
        stop_line.request(consumer="buttons", type=gpiod.LINE_REQ_DIR_IN)
        clear_line.request(consumer="buttons", type=gpiod.LINE_REQ_DIR_IN)
        
except Exception as e:
    print(f"GPIO initialization failed: {e}")
    sys.exit(1)


# Initialize keyboard device
found = False
for i in range(7):  # Check event0 through event6
    try:
        dev_path = f'/dev/input/event{i}'
        dev = InputDevice(dev_path)
        if dev.name == "2.4G Composite Devic":
            found = True
            print(f"Keyboard devide--> Got it, found in  {dev_path}")
            break
    except Exception as e:
        print(f"Error checking {dev_path}: {e}")
        continue

if not found:
    print("Keyboard initialization failed: Could not find '2.4G Composite Devic' in /dev/input/event0-6")
    chip.close()
    sys.exit(1)



# Global variables
display = drivers.Lcd()
keyboard_input = ""
status = "Starting..."
Counter = 0
prev_inp1 = 1

def myhook():
    rospy.loginfo("shutdown time from myhook() function!")  
    rospy.loginfo(f"Active threads: {threading.active_count()}")
    rospy.loginfo("there you go")
    os.system("\r\n") 
    sys.exit()

rospy.on_shutdown(myhook)

def callback_status(data):
    global Counter, status
    rospy.loginfo(rospy.get_caller_id() + " I heard: %s", data.data)
    status = data.data
    Counter += 1
    print(f"Counter: {Counter}")
    show_screen(status) 

def listener():
    rospy.init_node('raspi_node', anonymous=True)
    rospy.Subscriber("status", String, callback_status)
    rospy.on_shutdown(myhook)

def talker():
    global keyboard_input, prev_inp1
    pub = rospy.Publisher('Keyboard_Input', String, queue_size=10)
    rospy.loginfo(keyboard_input)
    pub.publish(keyboard_input)

def colorWipe(strip, color, wait_ms=50):
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms / 1000.0)

def show_screen(word):
    global keyboard_input
    display.lcd_clear()
    display.lcd_display_string(keyboard_input, 1)
    display.lcd_display_string(word, 2)

def keyboard_read_helper(dev):
    global keyboard_input, status
    print('------------------keyboard_read_helper started------------------')
    
    for event in dev.read_loop():
        try:
            rosgraph.Master('/rostopic').getPid()
        except Exception as inner_error:    #socket.error:
            print(f"Finishing the keyRead loop, error event: {inner_error}")
            break
        
        if event.type == ecodes.EV_KEY:
            key_data = categorize(event)
            print(key_data.keycode)

            if key_data.keystate == key_data.key_down:
                if key_data.keycode == 'KEY_F1':
                    print('toggle')
                    blink_rgb(0, 0, 1)  # blue
                elif key_data.keycode == 'KEY_ESC':
                    print('Exiting...')
                    show_screen("Leaving..")
                    blink_rgb(1, 0, 0)  # red
                    return
                elif key_data.keycode == 'KEY_BACKSPACE':
                    keyboard_input = keyboard_input[:-1]
                    print(f"Edited message: {keyboard_input}")
                elif key_data.keycode == 'KEY_SPACE':
                    keyboard_input += ' '
                else:
                    m = re.search('(?<=_)\w+', key_data.keycode)
                    if m:
                        keyboard_input += m.group(0)
                
                status = "Texting..."
                show_screen(status)
                time.sleep(0.5)

def check_buttons():
    """Check for button presses using libgpiod"""
    try:
        while True:
            # Check each button state
            if not start_line.get_value():
                Interrupt_Start(switch_start)
                while not start_line.get_value():  # Wait for release
                    time.sleep(0.05)
            
            if not stop_line.get_value():
                Interrupt_Stop(switch_stop)
                while not stop_line.get_value():
                    time.sleep(0.05)
            
            if not clear_line.get_value():
                Interrupt_Clear(switch_clear)
                while not clear_line.get_value():
                    time.sleep(0.05)
            
            time.sleep(0.05)  # Small delay to prevent CPU overload
    except KeyboardInterrupt:
        return

def Interrupt_Start(channel):
    global prev_inp1
    show_screen("Sending...")
    talker()
    blink_rgb(1, 1, 0)  # Yellow
    prev_inp1 = 0

def Interrupt_Clear(channel):
    global Counter, keyboard_input
    print("Clear button pressed")
    Counter = 0
    keyboard_input = ""
    blink_rgb(0, 0, 1)  # Blue
    show_screen("Clear...")

def Interrupt_Stop(channel):
    show_screen("STOP...")
    blink_rgb(1, 0, 0)  # Red
    os.system("sudo systemctl restart cnc.service")
    blink_rgb(1, 1, 1)  # White
    print(f"Process ID: {os.getpid()}")

def blink_rgb(r, g, b):
    for i in range(3):
        colorWipe(strip, Color(255*r, 255*g, 255*b))
        time.sleep(0.08)
        colorWipe(strip, Color(0, 0, 0))
        time.sleep(0.08)

def start_topic():
    global keyboard_input
    keyboard_input = "init"
    for _ in range(2):
        talker()
        time.sleep(0.2)
    keyboard_input = ""

if __name__ == '__main__':
    try:
        print("Initializing...")
        strip.begin()
        show_screen(status)
        blink_rgb(0, 1, 0)  # Green
        
        listener()
        start_topic()
        
        # Start button monitoring thread
        button_thread = threading.Thread(target=check_buttons)
        button_thread.daemon = True
        button_thread.start()
        
        keyboard_read_helper(dev)
        
    except KeyboardInterrupt:
        print("Keyboard interrupt")
    except rospy.ROSInterruptException:
        print("ROS interrupt exception")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        print("Cleaning up...")
        # Release GPIO resources
        start_line.release()
        stop_line.release()
        clear_line.release()
        chip.close()
        display.lcd_clear()

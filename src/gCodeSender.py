#!/usr/bin/env python3

import serial
import time
import io
import argparse
import rospy
from std_msgs.msg import String
import os
import sys

print ("Gcode sender is trying to open" )
parser = argparse.ArgumentParser(description='This is a basic gcode sender by Javier S.')
#parser.add_argument('-p','--port', help='Input USB port',required=True)
#parser.add_argument('-f','--file', help='Gcode file name',required=True)
parser.add_argument('-a','--port', help='Input USB port', default="/dev/ttyUSB0")
parser.add_argument('-b','--file', help='Gcode file name', default="/home/toby001/catkin_ws/src/cnc_marker/OutputFile.ngc")
#--args = parser.parse_args()
args, unknown = parser.parse_known_args()
## show values ##
print ("USB Port: %s" % args.port )
print ("Gcode file: %s" % args.file )
#Example--> ./gCodeSender.py -p /dev/ttyACM0 -f ./grbl.gcode
#>>reset_arduino()
#>>time.sleep(2) 
s = serial.Serial()

i = 1
while 1:
    print(i)
    
    try:
        i += 1
        print ("Trying to open the Port: %s" % args.port )
        s = serial.Serial(args.port,115200)
        spaces = "\r\n\r\n" 
        # Wake up grbl
        s.write(spaces.encode())
        #s.write("\r\n\r\n")
        time.sleep(2)   # Wait for grbl to initialize
        s.flushInput()  # Flush startup text in serial input
        break
    except:
        print("An exception occurred, could not Conect ")
        if i >= 5:
            print("try Tomorrow ....")
            time.sleep(1) 
            sys.exit(1) 
            break
    #resetSerial()




def callback(data):
  rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)

  if data.data == 'gcode_ready': #gcode_ready

      f = open(args.file,'r') # Open g-code file
      #f = open('grbl.gcode','r')

      # Stream g-code to grbl
      for line in f:
          l = line.strip() # Strip all EOL characters for consistency
          print ('Sending: ' + l)
          s.write((l + '\n').encode()) # Send g-code block to grbl
          grbl_out = s.readline() # Wait for grbl response with carriage return
          #--print (' : ' + grbl_out.strip()) 
          print (' : ' + grbl_out.strip().decode()) 

      # Wait here until grbl is finished to close serial port and file.
      #--input("  Press <Enter> to exit and disable grbl.")
      
      # Close file and serial port
      f.close()
      #s.close()
      reset_arduino()
      print ('### Gcode_Program sent ### ')
      rospy.loginfo("### Gcode_Program sent ### ")
      time.sleep(1)
  else:
      print ('Nothing to do yet :( ')


def listener():

    rospy.init_node('gCodeSender', anonymous=True)

    rospy.Subscriber("gcode_status", String, callback)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()
    
def reset_arduino():
    pass

def resetSerial():
    print ("ReTrying to open the Port: %s" % args.port )
    s = serial.Serial(args.port,115200)
    spaces = "\r\n\r\n" 
    # Wake up grbl
    s.write(spaces.encode())
    #s.write("\r\n\r\n")
    time.sleep(2)   # Wait for grbl to initialize
    s.flushInput()  # Flush startup text in serial input

if __name__ == '__main__':
    print ('****in the main ****')
    listener()
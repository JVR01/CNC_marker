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
parser.add_argument('-p','--port', help='Input USB port', default="/dev/ttyUSB0")
parser.add_argument('-f','--file', help='Gcode file name', default="/home/toby001/catkin_ws/src/cnc_marker/OutputFile.ngc")
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
      spaces = "\r\n\r\n" 
      s.write(spaces.encode())
      time.sleep(2)   # Wait for grbl to initialize
      s.flushInput()
      # Stream g-code to grbl
      eFile = open("/home/toby001/catkin_ws/src/cnc_marker/errors_gcodeSender.txt", "w")#"a" append, "w" overwrite
      eFile.close()
      eFile = open("/home/toby001/catkin_ws/src/cnc_marker/errors_gcodeSender.txt", "a")
      eFile.write('Errors found in the gCogeSender: ' + '\n')
      index =  0
      for line in f:
          index = index + 1
          l = line.strip() # Strip all EOL characters for consistency
          print ('Sending: ' + l)
          s.write((l + '\n').encode()) # Send g-code block to grbl
          pr = (l + '\n').encode()
          eFile.write('this was send->' + str(pr) +'<-'+'\n')
          #exception serial.SerialException
          grbl_out = s.readline() # Wait for grbl response with carriage return
          #--print (' : ' + grbl_out.strip()) 
          print (' : ' + grbl_out.strip().decode()) 

          answer = grbl_out.strip().decode()
          substring = "error"
          
          if substring in answer:
             spaces = "\r\n\r\n" 
             s.write(spaces.encode())
             time.sleep(2)   # Wait for grbl to initialize
             s.flushInput()
             print (' **************************************ERROR******************************************* ') 
             
             eFile.write('Error Sending line ' + str(index) + ' : ' + str(pr) + '\n')
             eFile.write('comentary: ' + answer + '\n')
             #
             #time.sleep(5)
      eFile.close()
      time.sleep(3)
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
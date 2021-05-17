#!/usr/bin/env python

# license removed for brevity
import rospy
import time
import logging
import threading
import sys
import os  #sys.exit(1)
from std_msgs.msg import String
from rospy import init_node, is_shutdown

Flag = True #useles but used for textInput
print("++++++-->manager started!!<----++++++++++++++++++++++++++++++++++++++++++++++++")

keyboard_input = "awesome"
status = "Idle"
enable_keyboard_input = True
gcode_status = ""

def myhook():
  rospy.loginfo("shutdown time!")  
  a = threading.active_count()
  rospy.loginfo(a)
  rospy.loginfo("there you got")
  #threading.keyboard_thread._stop_event.set() 
  os.system("\r\n") 
  sys.exit()
  sys.exit(1)

rospy.on_shutdown(myhook)
def callback_gcode(data):
    global gcode_status
    gcode_status = data.data
    rospy.loginfo("****************+")
    rospy.loginfo(rospy.get_caller_id() + " I heard: %s", data.data)
    time.sleep(5)

def callback(data):
    global keyboard_input
    global enable_keyboard_input
    rospy.loginfo("------------------------------")
    rospy.loginfo(rospy.get_caller_id() + " I heard: %s", data.data)
    keyboard_input = data.data
    time.sleep(1)

    print ("thanks for giving me " + keyboard_input)
    
    if keyboard_input == "Exit":
       enable_keyboard_input = False
       rospy.loginfo("***************LEAVIG manager NODE*********")
       os.system("\r\n") 
       sys.exit()
       sys.exit(1)
    else:
       print("keyboar_input changed")
       talker2()

def talker():
    global status
    pub = rospy.Publisher('status', String, queue_size=10)
    hello_str = "hello world %s" % rospy.get_time()
    #rospy.loginfo(keyboard_input)
    print(keyboard_input)
    pub.publish(status)
    
def talker2():
    pub2 = rospy.Publisher('keyboard', String, queue_size=10) 
    rospy.loginfo(keyboard_input)
    pub2.publish(keyboard_input)    
      
def listener():
    rospy.Subscriber("Keyboard_Input", String, callback)
    rospy.Subscriber("gcode_status", String, callback_gcode)
    rospy.loginfo("listener done")
    
    
if __name__ == '__main__':
    try:

        rospy.init_node('manager_node', anonymous=True)
        rate = rospy.Rate(5) # 10hz
        listener()
        
        while not rospy.is_shutdown():
           talker() #publishes status topic
           #rospy.loginfo("loop in the while")
           rate.sleep()
           #rospy.spin()
    except rospy.ROSInterruptException:
        pass
        
        

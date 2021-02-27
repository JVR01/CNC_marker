#!/usr/bin/env python3

# license removed for brevity
import rospy
import time
import logging
import threading
import sys

from std_msgs.msg import String
#import curses
from rospy import init_node, is_shutdown





keyboard_input = "awesome"
enable_keyboard_input = True


def callback(data):
    rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)
    time.sleep(1)

def talker():
    pub = rospy.Publisher('status', String, queue_size=10)
    #--rospy.init_node('talker', anonymous=True)
    rate = rospy.Rate(10) # 10hz
    #while not rospy.is_shutdown():
    hello_str = "hello world %s" % rospy.get_time()
    rospy.loginfo(hello_str)
    pub.publish(hello_str)
    
def talker2():
    pub2 = rospy.Publisher('keyboard', String, queue_size=10)
    hello_str = keyboard_input 
    rospy.loginfo(hello_str)
    pub2.publish(hello_str)    
    
    

def listener():

    #rospy.init_node('listener', anonymous=True)

    rospy.Subscriber("chatter", String, callback)
    rospy.loginfo("listener done")
    # spin() simply keeps python from exiting until this node is stopped
    #rospy.spin()
    
def get_keyboard_input(name):
    global keyboard_input
    global enable_keyboard_input
    
    print ("give something, please?")
    something = input("tell somesing:  ")
    print ("thanks for giving me " + something)
    
    if something == "Exit":
       print("gotaa Exit")
       keyboard_input = something
       enable_keyboard_input = False
       sys.exit()
    elif something == "":
       sys.exit()
    else:
       print("keyboar_input changed")
       keyboard_input = something
       talker2()
    #keyboard_input = something
    #talker2()
    enable_keyboard_input = False
    
    #time.sleep(5)
    
def keyboard_thread(x):
    global keyboard_input
    global enable_keyboard_input
    if x.is_alive() is True:
       rospy.loginfo("EStaaa vivo!!")
              #x.join()
    else:  
       enable_keyboard_input = True 
       x = threading.Thread(target=get_keyboard_input, args=(1,))
              
    if enable_keyboard_input  :
              
       try:
                  
           #"Main    : before creating thread"
           x.start()
           #wait for the thread to finish"
           #x.join()
           rospy.loginfo("finissshhhhh line!!")
           #enable_keyboard_input = True
       except:
           print ("Error: unable to start thread")    
    return x
    
    
if __name__ == '__main__':
    try:
        rospy.init_node('manager_node', anonymous=True)
        rate = rospy.Rate(10) # 10hz
        listener()
        x = threading.Thread(target=get_keyboard_input, args=(1,))
        
        while not rospy.is_shutdown():
           talker()
           rospy.loginfo("while")
           rospy.loginfo(keyboard_input)

           x = keyboard_thread(x)
           rate.sleep()
           '''
           here was the thread zeug
           '''        
           #rospy.spin()
    except rospy.ROSInterruptException:
        pass
        
        

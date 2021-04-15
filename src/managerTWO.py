#!/usr/bin/env python3

# license removed for brevity
import rospy
import time
import logging
import threading
import sys

import os  #sys.exit(1)


from std_msgs.msg import String
#import curses


from rospy import init_node, is_shutdown

Flag = True
 #testline
class MyThread(threading.Thread):
  
    # Thread class with a _stop() method. 
    # The thread itself has to check
    # regularly for the stopped() condition.
  
    def __init__(self, *args, **kwargs):
        super(MyThread, self).__init__(*args, **kwargs)
        self._stop = threading.Event()
  
    # function using _stop function
    def stop(self):
        print("stoped???")
        self._stop.set()
  
    def stopped(self):
        return self._stop.isSet()
  
    def run(self):
        while True:
            if self.stopped():
                return
            self = keyboard_thread(self)    
            print("Hello, world!")
            time.sleep(1)


keyboard_input = "awesome"
enable_keyboard_input = True
from pynput.keyboard import Key, Controller
def myhook():
  rospy.loginfo("shutdown time!")  
  #print "shutdown time!"

  #nodes = os.popen("rosnode list").readlines()
  #for i in range(len(nodes)):
    #nodes[i] = nodes[i].replace("\n","")

  #for node in nodes:
    #os.system("rosnode kill "+ node)
  a = threading.active_count()
  rospy.loginfo(a)
  rospy.loginfo("there you got")
  #threading.keyboard_thread._stop_event.set()

  rospy.loginfo(threading.__name__)
  if x.is_alive() is True:
    rospy.loginfo("Thread active and listening")
    #x._block
    #threading.Thread._block
  #t1.stop()
  keyboard = Controller()
  keyboard.press('a')
  keyboard.press('a')
  keyboard.press('b')
  sys.exit()
  #keyboard.press(Key.enter)
  #keyboard.press('ZZZ')
  #keyboard.press(Key.enter)
  #Key.enter
  
  os.system("\r\n") 
  
  sys.exit(1)

rospy.on_shutdown(myhook)

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

    rospy.Subscriber("manager_listener", String, callback)
    rospy.loginfo("listener done")
    # spin() simply keeps python from exiting until this node is stopped
    #rospy.spin()
    
def get_keyboard_input(name):
    global keyboard_input
    global enable_keyboard_input
    
    print ("give something, please?")
    if Flag == True:
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
       rospy.loginfo("Thread active and listening")
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
           print ("Error: unable to start thread again")    
    return x
    
    
if __name__ == '__main__':
    try:

        #t1 = MyThread()
        
        #t1.start()
        #time.sleep(5)
        #t1.stop()
        #t1.join()

        rospy.init_node('manager_node', anonymous=True)
        rate = rospy.Rate(10) # 10hz
        listener()
        x = threading.Thread(target=get_keyboard_input, args=(1,))
        #x.start()

        #x = keyboard_thread(x)
        while not rospy.is_shutdown():
           talker() #publishes status topic
           rospy.loginfo("loop in the while")
           rospy.loginfo(keyboard_input)

           x = keyboard_thread(x)
           #if x.is_alive() is False:
              #x.start()
           rate.sleep()
                 
           #rospy.spin()
    except rospy.ROSInterruptException:
        pass
        
        

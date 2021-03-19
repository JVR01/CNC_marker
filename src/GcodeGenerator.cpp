#include "ros/ros.h"
#include "std_msgs/String.h"
#include <sstream>
#include <fstream>
#include "lib/rapidxml-1.13/rapidxml.hpp"


//#include <iostream>
//using namespace std;

ros::Publisher chatter_pub;
int count = 0;
std_msgs::String status;
std::ofstream fs("src/cnc_marker/src/GcodeText.txt"); //writes out the results
char valid_chars[] = { 'A', 'B', 'C'  }; //'\0'

//myfile.close();

/**
 * This tutorial demonstrates simple sending of messages over the ROS system.
 */
//void pubstatus(){}
bool input_valid(std::string const &message)
{
  bool valid = true;
  std::string Message = message;
  
  int sizeOfArray = sizeof(valid_chars) / sizeof(valid_chars[0]);
  
  std::string validcharacters(valid_chars);
  for ( std::string::iterator it=Message.begin(); it!=Message.end(); ++it)
  {
     //std::cout << *it;
     //ROS_INFO("%s\n", message.c_str());
     std::string character; 
     character += *it;
     bool on_thelist = false;
     if( validcharacters.find(character) != std::string::npos )
       {on_thelist = true;}
     else
       {on_thelist= false;valid=false;} 
  }
   //s1.find(s2) != std::string::npos
   //if( (message.find("C") != std::string::npos) | ( message.find("D")!= std::string::npos)  ){valid = true;}
  
  ROS_INFO("%s", message.c_str());
  return valid; 
}

void pubstatus(std::string msg_str)
{
  //ros::Rate loop_rate(10);
  std_msgs::String msg;
  std::stringstream ss;
  ss << "hello worldio " << count;
  msg.data = ss.str();
  msg.data = msg_str;
  ROS_INFO("%s", msg.data.c_str());
  chatter_pub.publish(msg);
  //ros::spinOnce();
  //loop_rate.sleep();
}

void generate_code(std::string const & message)
{
  for (int i = 0; i <= 100; i++)
  {

    std::stringstream ss;
    ss << "working " << i;
    //std::string words =  "working "+ i;
    ROS_INFO("%s", ss.str().c_str()); //status.data.c_str()
  }
  //fs << "Test number: " << ss.str() << std::endl;
  fs << "Test number: " << message << std::endl;
  std::string  msg = "gcode_ready";
  pubstatus(msg);

}

void chatterCallback(const std_msgs::String::ConstPtr &msg)
{
  ++count;
  ROS_INFO("GcodeGenerator heard: [%s]", msg->data.c_str());
  

  std::string message = msg->data;
  if (input_valid(message))
  {
    generate_code(message);
  }
  else
  {
    pubstatus("wrong input");
  }
  ros::Duration(5.0).sleep();
}


int main(int argc, char **argv)
{
  ros::init(argc, argv, "keybord_listener");
  ros::NodeHandle n;
  ros::Rate loop_rate(10);
  ros::Subscriber sub = n.subscribe("keyboard", 1000, chatterCallback);
  chatter_pub = n.advertise<std_msgs::String>("gcode_status", 1000);

  ros::spinOnce();

  while (ros::ok())
  {
    //std_msgs::String msg;
    std::stringstream ss;
    ss << "idleee " << count;
    status.data = ss.str();
    ROS_INFO("%s", status.data.c_str());
    chatter_pub.publish(status);
    ros::spinOnce();
    loop_rate.sleep();
    //++count;
  }
  return 0;
}

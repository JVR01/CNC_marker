#include "ros/ros.h"
#include "std_msgs/String.h"
#include <sstream>
#include <fstream>
#include "lib/rapidxml-1.13/rapidxml.hpp"

ros::Publisher chatter_pub;
int count = 0;
std_msgs::String status;
std::ofstream fs("src/cnc_marker/src/GcodeText.txt"); //writes out the results

//myfile.close();

/**
 * This tutorial demonstrates simple sending of messages over the ROS system.
 */

void generate_code(std::string message)
{
  for (int i = 0; i <= 100; i++)
  {

    std::stringstream ss;
    ss << "working " << i;
    //std::string words =  "working "+ i;
    ROS_INFO("%s", ss.str().c_str()); //status.data.c_str()
    fs << "Test number: " << ss.str() << std::endl;
  }
}

void chatterCallback(const std_msgs::String::ConstPtr &msg)
{
  ++count;
  ROS_INFO("I heard: [%s]", msg->data.c_str());

  std::string mesage = msg->data;

  generate_code(mesage);
}

void pubstatus(std::string msgg)
{
  ros::Rate loop_rate(10);
  std_msgs::String msg;
  std::stringstream ss;
  ss << "hello worldio " << count;
  msg.data = ss.str();
  ROS_INFO("%s", msg.data.c_str());
  chatter_pub.publish(msg);
  ros::spinOnce();
  loop_rate.sleep();
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

#include "ros/ros.h"
#include "std_msgs/String.h"
#include <sstream>
#include <fstream>
#include "lib/rapidxml-1.13/rapidxml.hpp"

//#include "src/lib/text_parser/csv_row.h"
#include "lib/text_parser/csv_row.h"
#include "lib/text_parser/gcode_parser.h"

//#include <iostream>
#include "lib/text_parser/gcode_parser.h"

//using namespace std;

ros::Publisher chatter_pub;
int count = 0;
std_msgs::String status;
std::ofstream fs("src/cnc_marker/src/GcodeText.txt"); //writes out the results
char valid_chars[] = { 'A', 'B', 'C', 'M' , 'R' }; //'\0'
bool validate_next = true;
CSVRow roww;

//std::string char_path = "/home/toby001/catkin_ws/src/cnc_marker/src/Characters/";
//std::string Out_Path = "/home/toby001/catkin_ws/src/cnc_marker/";

std::string char_path = "/home/tamer/ros_catkin_ws/src/CNC_marker/src/Characters/";
std::string Out_Path = "/home/tamer/ros_catkin_ws/src/CNC_marker/";

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
  std::cout << ">char_path: " << char_path << std::endl;
  std::cout << ">Out_Path: " << Out_Path << std::endl;
  std::cout << " "  << std::endl;

  GcodeParser GCode(char_path, Out_Path);
  GCode.add_start_code();
  //int U = GCode.add_character("A");
  //U = GCode.add_character(" ");
  //U = GCode.add_character(";");
  //U = GCode.add_character("B");
  //U = GCode.add_character("C");
  int U = GCode.add_phrase(message);
  
  //GCode.add_end_code();
  fs << "result U: " << U << std::endl;
  fs << "char_Path:" << GCode.getCharPath()<< std::endl;

  std::cout << "Bad characters U: " << U << std::endl;
  if(U>0U)
  {
    return; //so that it does not publish the msg with wron chars.
  }

  /*for (int i = 0; i <= 100; i++)
  {

    std::stringstream ss;
    ss << "working " << i;
    //std::string words =  "working "+ i;
    ROS_INFO("%s", ss.str().c_str()); //status.data.c_str()
  }*/
  
  //fs << "Test number: " << ss.str() << std::endl;
  fs << "Test number: " << message << std::endl;
  std::string  msg = "gcode_ready";
  //---->pubstatus(msg); //original comand
  if (validate_next)
  {
    pubstatus(msg);
  }
  else
  {
    pubstatus("Bussy now");
  }
}

void chatterCallback(const std_msgs::String::ConstPtr &msg)
{
  ++count;
  ROS_INFO("GcodeGenerator heard: [%s]", msg->data.c_str());

  std::cout << ">GcodeGenerator heard: " << msg->data.c_str() << std::endl;
  
  std::string message = msg->data;
  if (input_valid(message))
  {
    pubstatus("Input valid");
    generate_code(message);
  }
  else
  {
    pubstatus("Wrong input");
  }
  ros::Duration(1.0).sleep();
}

void Callback_Sender(const std_msgs::String::ConstPtr &msg)
{
 
  //ROS_INFO("GcodeGenerator, heard sender: [%s]", msg->data.c_str());
  
  std::string message = msg->data;
  if (message == "Terminated")
  {
    validate_next = true;
  }
  else
  {
    validate_next = false;
    //pubstatus("Bussy now");
  }
}


int main(int argc, char **argv)
{

  std::cout << "You have entered " << argc << " arguments:" << "\n";

    
  if(argc > 1)
  {
  for (int i = 0; i < argc; ++i){
        std::cout <<"Arg"<<i+1<<" :"<< argv[i] << "\n";
  }  
  char_path = argv[1];
  Out_Path = argv[2];     
  }
  else if(argc >= 3)
  {
    std::cout << "WRONG number of" << argc << " ARGUMENTS" << "\n";
    return 0;
  }

  ros::init(argc, argv, "keybord_listener");
  ros::NodeHandle n;
  ros::Rate loop_rate(5); //5Hz
  ros::Subscriber sub = n.subscribe("keyboard", 1000, chatterCallback);
  ros::Subscriber sub_status = n.subscribe("sender_status", 1000, Callback_Sender);
  chatter_pub = n.advertise<std_msgs::String>("gcode_status", 1000);
  chatter_pub.publish(status);
  ros::spinOnce();

  while (ros::ok())
  {
    //std_msgs::String msg;
    std::stringstream ss;
    ss << "idleee " << count;
    status.data = ss.str();
    //---->ROS_INFO("%s", status.data.c_str());
    //chatter_pub.publish(status);
    ros::spinOnce();
    loop_rate.sleep();
    //ros::Duration(0.1).sleep();
    //++count;
  }
  return 0;
}

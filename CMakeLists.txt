cmake_minimum_required(VERSION 3.0.2)
project(cnc_marker)


find_package(catkin REQUIRED COMPONENTS
  roscpp
  rospy
  std_msgs
  genmsg
  message_generation
)
#find_package(roscpp REQUIRED)
#find_package(std_msgs REQUIRED)

catkin_package(
#  INCLUDE_DIRS include
#  LIBRARIES cnc_marker
#  CATKIN_DEPENDS roscpp rospy std_msgs
#  DEPENDS system_lib
)


include_directories(
# include
  ${catkin_INCLUDE_DIRS}
)

set( project_sources
   src/lib/text_parser/csv_row.cpp
   src/lib/text_parser/gcode_parser.cpp
)
#include_directories(${roscpp_INCLUDE_DIRS})
#include_directories(${std_msgs_INCLUDE_DIRS})

add_executable(GcodeGenerator src/GcodeGenerator.cpp ${project_sources})
target_link_libraries(GcodeGenerator ${roscpp_LIBRARIES} ${std_msgs_LIBRARIES})

add_executable(listenercpp src/listenercpp.cpp)
target_link_libraries(listenercpp ${roscpp_LIBRARIES} ${std_msgs_LIBRARIES})


# (optional) Install the executables.
#install(TARGETS GcodeGenerator listenercpp DESTINATION bin)
install(TARGETS GcodeGenerator DESTINATION build)
#install(DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/src/ DESTINATION nix)

cmake_minimum_required(VERSION 3.12)

project(test_gcode_parser)


# Create a list with all .cpp source files
set( project_sources
   main.cpp
   gcode_parser.cpp
)


add_executable(${PROJECT_NAME}
  ${project_sources}
)



#---------------------------------------------

#set(CMAKE_INCLUDE_CURRENT_DIR ON)
#set(CMAKE_AUTOMOC ON)




# Create executable with all necessary source files


/***********************************************************************
This sketch compiles and uploads Grbl to your 328p-based Arduino! 

To use:
- First make sure you have imported Grbl source code into your Arduino
  IDE. There are details on our Github website on how to do this.

- Select your Arduino Board and Serial Port in the Tools drop-down menu.
  NOTE: Grbl only officially supports 328p-based Arduinos, like the Uno.
  Using other boards will likely not work!

- Then just click 'Upload'. That's it!

For advanced users:
  If you'd like to see what else Grbl can do, there are some additional
  options for customization and features you can enable or disable. 
  Navigate your file system to where the Arduino IDE has stored the Grbl 
  source code files, open the 'config.h' file in your favorite text 
  editor. Inside are dozens of feature descriptions and #defines. Simply
  comment or uncomment the #defines or alter their assigned values, save
  your changes, and then click 'Upload' here. 
  
https://github.com/gnea/grbl/wiki/Grbl-v1.1-Configuration
***********************************************************************/

#include <grbl.h>

//**********+this chees will work
//I just altered this File :D JVR, It works. Thoght the important files are in 
//..\Arduino\libraries\grbl-mi
// Do not alter this file!
//Chexk the absolte maschine Zero!!
//G92 X0 Y0 Z0
//G10 P0 L20 X0 Y0 Z0
/*
 * M5 brings the servo to 0° CW
 * M4 brings the servo to the last set Sx
 * M3 Sx    -->  0<x<180 brings the servo to x°       x=70 for servo Up CNC-Engraver
 */
 

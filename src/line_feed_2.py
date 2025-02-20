#!/usr/bin/env python3
import serial
import sys
#usage>> toby001@ubuntu:~/catkin_ws$ ./src/CNC_marker/src/line_feed_2.py /dev/ttyUSB0 /home/toby001/catkin_ws/src/CNC_marker/src/Characters/batman.gcode nonstop
last_response = "ok"

def send_gcode(device_path, gcode_file_path, nonstop=False):
    try:
        # Open the serial connection to the device
        ser = serial.Serial(device_path, baudrate=115200, timeout=1)
        print(f"Connected to {device_path}")

        # Open the G-code file
        with open(gcode_file_path, 'r') as file:
            lines = file.readlines()

        # Send each line of G-code
        for line in lines:
            line = line.strip()  # Remove leading/trailing whitespace
            if line:  # Skip empty lines
                print(f"Sending: {line}")
                ser.write((line + '\n').encode())  # Send the line to the device

                # Read and print the response from the device
                response = ser.readline().decode().strip()
                last_response = response

                if response:
                    print(f"Response: {response}")
                
                #if  last_response != "ok":
                 #   print(f"non quite ok Response: {last_response}")
                  #  input("Not quite ok, press Enter to send the next line...")

                # Wait for user input if not in nonstop mode
                if not nonstop:
                    input("Press Enter to send the next line...")

        print("G-code file sent successfully!")

    except FileNotFoundError:
        print(f"Error: G-code file not found at {gcode_file_path}")
    except serial.SerialException as e:
        print(f"Error: Could not connect to {device_path}. {e}")
    finally:
        if 'ser' in locals() and ser.is_open:
            ser.close()
            print("Serial connection closed.")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python send_gcode.py <device_path> <gcode_file_path> [nonstop]")
    else:
        device_path = sys.argv[1]
        gcode_file_path = sys.argv[2]
        nonstop = (len(sys.argv) > 3 and sys.argv[3].lower() == "nonstop")
        send_gcode(device_path, gcode_file_path, nonstop)

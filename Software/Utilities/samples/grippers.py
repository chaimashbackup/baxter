#!/usr/bin/python3

import time

# rospy - ROS Python API
import rospy

# baxter_interface - Baxter Python API
import baxter_interface

# initialize our ROS node, registering it with the Master
rospy.init_node('Hello_Baxter')

# get gripper inteface
left = baxter_interface.Gripper('left')
right = baxter_interface.Gripper('right')


def open_grippers():
    print("Opening both grippers...")
    left.open()
    right.open()


def close_grippers():
    print("Closing both grippers...")
    left.close()
    right.close()


# calibrating grippers
print("Calibrating left gripper")
left.calibrate()
print("Calibrating right gripper")
right.calibrate()

# reset to open state
open_grippers()
time.sleep(5)


print("Testing opening and closing of both grippers at once...")
for _action in range(3):
    close_grippers()
    time.sleep(5)
    open_grippers()
    time.sleep(5)

# a small delay state
time.sleep(5)

print("Testing opening and closing grippers one by one...")
for _action in range(3):
    print("Closing right gripper...")
    right.close()
    time.sleep(1)
    print("Right gripper position: ", right.position())
    time.sleep(5)
    print("Closing left gripper...")
    left.close()
    time.sleep(1)
    print("Left gripper position: ", left.position())
    time.sleep(5)
    print("Opening right gripper...")
    right.open()
    time.sleep(5)
    print("Opening left gripper...")
    left.open()
    time.sleep(5)

open_grippers()

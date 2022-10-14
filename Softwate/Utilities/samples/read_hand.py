#!/usr/bin/python3

# rospy - ROS Python API
import rospy
import time

# baxter_interface - Baxter Python API
import baxter_interface

# initialize our ROS node, registering it with the Master
rospy.init_node('Baxter_Hand_Control')

# create an instance of baxter_interface's Limb class
left_limb = baxter_interface.Limb('left')
right_limb = baxter_interface.Limb('right')

# get limb's current joint angles
left_angles = left_limb.joint_angles()
right_angles = right_limb.joint_angles()


# print the current joint angles
print("Left limb angles:\n", left_angles)
print("Right limb angles:\n", right_angles)

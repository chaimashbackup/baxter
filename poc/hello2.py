#!/usr/bin/python3

# rospy - ROS Python API
import rospy

# baxter_interface - Baxter Python API
import baxter_interface

# initialize our ROS node, registering it with the Master
rospy.init_node('Hello_Baxter')

# create an instance of baxter_interface's Limb class
limb = baxter_interface.Limb('left')

# Baxter wants to say hello, let's wave the arm

# store the first wave position
wave_1 = {
    'left_e0': -1.5976409905826585,
    'left_e1': 1.7199759584165202,
    'left_s0': -0.002684466378799474,
    'left_s1': -0.3401602397135905,
    'left_w0': -2.3094080761614904,
    'left_w1': 2.0958012514484463,
    'left_w2': 0.8601797268067457
}

# store the second wave position
wave_2 = {
    'left_e0': -1.5792332211280335,
    'left_e1': 1.7993594641895903,
    'left_s0': -0.03528155812136451,
    'left_s1': -0.2684466378799474,
    'left_w0': -1.3334127998693959,
    'left_w1': 1.4695535947942264,
    'left_w2': 1.039655478989339
}

# wave once
for _move in range(1):
    limb.move_to_joint_positions(wave_1)
    limb.move_to_joint_positions(wave_2)

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

_left_hand_default_angles = {
    'left_e0': 0.030366517587187225,
    'left_e1': 0.5092856895242841,
    'left_s0': 0.05772260551181585,
    'left_s1': 1.0470048271610723,
    'left_w0': -1.489176886014258,
    'left_w1': -0.03345367769963126,
    'left_w2': 0.07099728252938409
}

left_hand_default_angles = {
    'left_e0': -1.1884516154142244,
    'left_e1': 1.9378012302962488,
    'left_s0': -0.08206797215186963,
    'left_s1': -0.998237997716433,
    'left_w0': 0.668432128321069,
    'left_w1': 1.0270001374892845,
    'left_w2': -0.5019952128355016
}

_right_hand_default_angles = {
    'right_e0': 0.028473973636050864,
    'right_e1': 0.5092396318344825,
    'right_s0': -0.0684713005961628,
    'right_s1': 1.0470028136974792,
    'right_w0': -1.349470679306095,
    'right_w1': -0.029485081110774303,
    'right_w2': -1.3088317331432728
}

right_hand_default_angles = {
    'right_e0': 1.2210487071567893,
    'right_e1': 1.942019677462934,
    'right_s0': 0.05714078434873166,
    'right_s1': -0.961422458807183,
    'right_w0': -0.7332428166092277,
    'right_w1': 0.9261409006858186,
    'right_w2': 0.4536748180171111
}

# print the joint angle command
print("Moving left limb to:\n", left_hand_default_angles)
print("Moving right limb to:\n", right_hand_default_angles)

left_limb.move_to_joint_positions(left_hand_default_angles)
right_limb.move_to_joint_positions(right_hand_default_angles)

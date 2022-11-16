#!/usr/bin/python3

# rospy - ROS Python API
import rospy
import time
import json
import sys
import os.path

# baxter_interface - Baxter Python API
# import baxter_interface
from baxter_interface import Limb
from baxter_interface import Gripper



# initialize our ROS node, registering it with the Master


# create an instance of baxter_interface's Limb class
# left_limb = Limb('left')

path = "./initPos.json"
path1 = "./coord.json"
path2 = "./coord2.json"
initData = None
coordPos0 = None
coordPos1 = None


angles = {
    'left_e0': 0.0,
    'left_e1': 0.0,
    'left_s0': 0.0,
    'left_s1': 0.0,
    'left_w0': 0.0,
    'left_w1': 0.0,
    'left_w2': 0.0,
}


def exists(path):
    try:
        os.stat(path)
    except OSError:
        return False
    return True

def setAngles(data, angles):
    j = 2
    for i in angles.keys():
        angles[i] = data[j]
        j += 1
    print(angles)

def clearAngles(angles):
    for i in angles.keys():
        angles[i] = 0.0

if __name__ == '__main__':
    rospy.init_node('BaxterCoord', anonymous=True)
    left_limb = Limb('left')
    left_gripper = Gripper('left')

    if exists(path) and exists(path2):
        with open(path, 'r') as jsonFile:
            initData = json.load(jsonFile)
        with open(path1, 'r') as jsonFile:
            coordPos0 = json.load(jsonFile)
        with open(path2, 'r') as jsonFile:
            coordPos1 = json.load(jsonFile)
    

    if initData is not None and coordPos0 is not None and coordPos1 is not None:
        for i in range(len(coordPos0)):
            print("____%s____", i)
            setAngles(initData[0], angles)
            
            if angles['left_e0'] != 0.0:
                time.sleep(1)
                # angles['left_w2'] = 0.0
                left_limb.move_to_joint_positions(angles)
                clearAngles(angles)

            setAngles(coordPos1[i], angles)
            time.sleep(1)
            if angles['left_e0'] != 0.0:
                left_limb.move_to_joint_positions(angles)
                clearAngles(angles)

            setAngles(coordPos0[i], angles)
            time.sleep(1)
            if angles['left_e0'] != 0.0:
                left_limb.move_to_joint_positions(angles)
                clearAngles(angles)
            
            left_gripper.close(block=False)
            time.sleep(1)

            setAngles(coordPos1[i], angles)
            time.sleep(1)
            if angles['left_e0'] != 0.0:
                left_limb.move_to_joint_positions(angles)
                clearAngles(angles)

            left_gripper.open(block=False)

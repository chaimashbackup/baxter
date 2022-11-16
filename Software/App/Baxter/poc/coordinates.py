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

from multiprocessing.connection import wait
import os
import cv2, cv_bridge 
from baxter_interface.camera import CameraController

from baxter_core_msgs.srv import (
    CloseCamera,
    ListCameras,
    OpenCamera,
)

from sensor_msgs.msg import Image
from std_msgs.msg import Bool



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



class camModule():
    bridge = cv_bridge.CvBridge() 
    image = None
    def __init__(self) -> None:
        rospy.Subscriber('/cameras/left_hand_camera/image', Image, self.camAction)

    def camAction(self, data):
        self.image = self.bridge.imgmsg_to_cv2(data, desired_encoding="passthrough")

    def getImage(self, name):
        if self.image is not None:
            cv2.imwrite(name, self.image)
        else:
            print("image not found")


if __name__ == '__main__':

    dataset = "./dataset/image"
    rospy.init_node('BaxterCoord', anonymous=True)
    left_limb = Limb('left')
    left_gripper = Gripper('left')

    cm = camModule()

    time.sleep(5)
    if exists(path) and exists(path2):
        with open(path, 'r') as jsonFile:
            initData = json.load(jsonFile)
        with open(path1, 'r') as jsonFile:
            coordPos0 = json.load(jsonFile)
        with open(path2, 'r') as jsonFile:
            coordPos1 = json.load(jsonFile)
    
    if initData is None:
        print(1)

    if coordPos0 is None:
        print(2)
    if coordPos1 is None:
        print(3)

    if initData is not None and coordPos0 is not None and coordPos1 is not None:

        
        setAngles(initData[0], angles)
        
#         if angles['left_e0'] != 0.0:
#             time.sleep(1)
#             left_limb.move_to_joint_positions(angles)
#             clearAngles(angles)

#             setAngles(coordPos1[0], angles)
#             time.sleep(1)
#             if angles['left_e0'] != 0.0:
#                 left_limb.move_to_joint_positions(angles)
#                 clearAngles(angles)

#             setAngles(coordPos0[0], angles)
#             time.sleep(1)
#             if angles['left_e0'] != 0.0:
#                 left_limb.move_to_joint_positions(angles)
#                 clearAngles(angles)
            
#             left_gripper.close(block=False)
#             time.sleep(1)

#             setAngles(coordPos1[0], angles)
#             time.sleep(1)
#             if angles['left_e0'] != 0.0:
#                 left_limb.move_to_joint_positions(angles)
#                 clearAngles(angles)

#             setAngles(coordPos0[0], angles)
#             time.sleep(1)
#             if angles['left_e0'] != 0.0:
#                 left_limb.move_to_joint_positions(angles)
#                 clearAngles(angles)

#             left_gripper.open(block=False)
#             time.sleep(1)

#             setAngles(coordPos1[0], angles)
#             time.sleep(1)
#             if angles['left_e0'] != 0.0:
#                 left_limb.move_to_joint_positions(angles)
#                 clearAngles(angles)


# ###


#             setAngles(coordPos0[0], angles)
#             time.sleep(1)
#             if angles['left_e0'] != 0.0:
#                 left_limb.move_to_joint_positions(angles)
#                 clearAngles(angles)
            
#             left_gripper.close(block=False)
#             time.sleep(1)

#             setAngles(coordPos1[1], angles)
#             time.sleep(1)
#             if angles['left_e0'] != 0.0:
#                 left_limb.move_to_joint_positions(angles)
#                 clearAngles(angles)

#             setAngles(coordPos0[1], angles)
#             time.sleep(1)
#             if angles['left_e0'] != 0.0:
#                 left_limb.move_to_joint_positions(angles)
#                 clearAngles(angles)

#             left_gripper.open(block=False)
#             time.sleep(1)

#             setAngles(coordPos1[1], angles)
#             time.sleep(1)
#             if angles['left_e0'] != 0.0:
#                 left_limb.move_to_joint_positions(angles)
#                 clearAngles(angles)

        for i in range(len(coordPos0)):
        # for i in range(3):
            if i <= 2:
                continue
            print(i)
            w = 0.0
            for j in range(8):
                print("____%s____", str(i))
                setAngles(initData[0], angles)
                
                
                if angles['left_e0'] != 0.0:
                    time.sleep(1)
                    # angles['left_w2'] = 0.0
                    left_limb.move_to_joint_positions(angles)
                    clearAngles(angles)
                print()
                cm.getImage((dataset + str(i) + str(j) + ".jpg"))

                if j != 0:
                    w = (float(j) / 10.0) * 2


                setAngles(coordPos1[i], angles)
                time.sleep(1)
                if angles['left_e0'] != 0.0:
                    angles['left_w2'] = angles['left_w2'] + w
                    left_limb.move_to_joint_positions(angles)
                    clearAngles(angles)

                setAngles(coordPos0[i], angles)
                time.sleep(1)
                if angles['left_e0'] != 0.0:
                    angles['left_w2'] = angles['left_w2'] + w
                    left_limb.move_to_joint_positions(angles)
                    clearAngles(angles)
                
                left_gripper.close(block=False)
                time.sleep(1)

                
                w = (float(j + 1) / 10.0) * 2

                setAngles(coordPos0[i], angles)
                time.sleep(1)
                if angles['left_e0'] != 0.0:
                    angles['left_w2'] = angles['left_w2'] + w
                    left_limb.move_to_joint_positions(angles)
                    clearAngles(angles)

                left_gripper.open(block=False)

                setAngles(coordPos1[i], angles)
                time.sleep(1)
                if angles['left_e0'] != 0.0:
                    angles['left_w2'] = angles['left_w2'] + w
                    left_limb.move_to_joint_positions(angles)
                    clearAngles(angles)
            
            setAngles(initData[0], angles)
            if angles['left_e0'] != 0.0:
                time.sleep(1)
                # angles['left_w2'] = 0.0
                left_limb.move_to_joint_positions(angles)
                clearAngles(angles)
            
            if i == (len(coordPos0) - 1):
                break

            setAngles(coordPos1[i], angles)
            time.sleep(1)
            if angles['left_e0'] != 0.0:
                angles['left_w2'] = angles['left_w2'] + w
                left_limb.move_to_joint_positions(angles)
                clearAngles(angles)

            setAngles(coordPos0[i], angles)
            time.sleep(1)
            if angles['left_e0'] != 0.0:
                angles['left_w2'] = angles['left_w2'] + w
                left_limb.move_to_joint_positions(angles)
                clearAngles(angles)

            left_gripper.close(block=False)

            w = 0.0

            setAngles(coordPos1[i + 1], angles)
            time.sleep(1)
            if angles['left_e0'] != 0.0:
                angles['left_w2'] = angles['left_w2'] + w
                left_limb.move_to_joint_positions(angles)
                clearAngles(angles)

            setAngles(coordPos0[i + 1], angles)
            time.sleep(1)
            if angles['left_e0'] != 0.0:
                angles['left_w2'] = angles['left_w2'] + w
                left_limb.move_to_joint_positions(angles)
                clearAngles(angles)
            
            left_gripper.open(block=False)

            setAngles(coordPos1[i + 1], angles)
            time.sleep(1)
            if angles['left_e0'] != 0.0:
                angles['left_w2'] = angles['left_w2'] + w
                left_limb.move_to_joint_positions(angles)
                clearAngles(angles)
            

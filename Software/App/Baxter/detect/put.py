#!/usr/bin/env python3

import cv2
import torch
import numpy as np 
import onnx
import onnxruntime as rt
from dataclasses import dataclass
import imutils

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
from DtDetection import DtDetection
from DtGetNumPosition import DtGetNumPosition
from DtCameraBaxter import camModule

dirname = os.path.dirname(__file__)
coordPath = {   "init": os.path.join(dirname, "./json/initPos.json"),
                "pose0": os.path.join(dirname, "./json/Pos0.json"),
                "pose1": os.path.join(dirname, "./json/Pos1.json"),
                "lastState": os.path.join(dirname, "./json/lastState.json"),
            }


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

lastState = {
    'pickUp'  : False,
    'gripper' : False,
    'rotation': 0.0,
    'numPose' : 0,
    'object'  : 0
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
    rospy.init_node('put', anonymous=True)
    left_limb = Limb('left')
    left_gripper = Gripper('left')


    if exists(coordPath['lastState']):
        with open(coordPath['lastState'], 'r') as jsonFile:
            lastState = json.load(jsonFile)
            print(lastState)
    else:
        with open(coordPath['lastState'], 'w') as jsonFile:
            json.dump(lastState, jsonFile, indent=4)

    if exists(coordPath['init']) and exists(coordPath['pose0']) and exists(coordPath['pose1']):
        with open(coordPath['init'], 'r') as jsonFile:
            initData = json.load(jsonFile)
        with open(coordPath['pose0'], 'r') as jsonFile:
            coordPos0 = json.load(jsonFile)
        with open(coordPath['pose1'], 'r') as jsonFile:
            coordPos1 = json.load(jsonFile)

        if initData is None or coordPos0 is None or coordPos1 is None:
            sys.exit(1)
    
    if lastState['pickUp']:
        if lastState['gripper']:
            setAngles(coordPos0[lastState['numPose']], angles)
            if angles['left_e0'] != 0.0:
                angles['left_w2'] = angles['left_w2'] + lastState['rotation']
                left_limb.move_to_joint_positions(angles)
                clearAngles(angles)
            time.sleep(1)

            left_gripper.open(block=False)

            with open(coordPath['lastState'], 'w') as jsonFile:
                json.dump(lastState, jsonFile, indent=4)

            setAngles(coordPos1[lastState['numPose']], angles)
            if angles['left_e0'] != 0.0:
                angles['left_w2'] = angles['left_w2'] + lastState['rotation']
                left_limb.move_to_joint_positions(angles)
                clearAngles(angles)
            time.sleep(1)


            setAngles(initData[0], angles)
            if angles['left_e0'] != 0.0:
                left_limb.move_to_joint_positions(angles)
                clearAngles(angles)
            time.sleep(1)

            lastState['gripper'] = False
            lastState['pickUp'] = False
            lastState['object'] = 0
            lastState['numPose'] = 0

            with open(coordPath['lastState'], 'w') as jsonFile:
                json.dump(lastState, jsonFile, indent=4)

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


coordPath = {   "init": "./json/initPos.json", 
                "pose0": "./json/Pose0.json",
                "pose1": "./json/Pose1.json",
                "lastState": "./json/lastState.json" 
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




def detect(numObject:int = 1):

    DtD     = DtDetection('./models/roboBaxter.onnx', "../../../ThirdParty/yolov5")
    DtObj1  = DtDetection('./models/object1.onnx', "../../../ThirdParty/yolov5")
    DtObj2  = DtDetection('./models/object2.onnx', "../../../ThirdParty/yolov5")
    

    rospy.init_node('obj1', anonymous=True)
    left_limb = Limb('left')
    left_gripper = Gripper('left')

    if exists(coordPath['init']) and exists(coordPath['pose0']) and exists(coordPath['pose1']):
        with open(coordPath['init'], 'r') as jsonFile:
            initData = json.load(jsonFile)
        with open(coordPath['pose0'], 'r') as jsonFile:
            coordPos0 = json.load(jsonFile)
        with open(coordPath['pose1'], 'r') as jsonFile:
            coordPos1 = json.load(jsonFile)

        if initData is None or coordPos0 is None or coordPos1 is None:
            sys.exit(1)


    if exists(coordPath['lastState']):
        with open(coordPath['lastState'], 'r') as jsonFile:
            lastState = json.load(jsonFile)
            print(lastState)
    else:
        with open(coordPath['lastState'], 'w') as jsonFile:
            json.dump(lastState, jsonFile, indent=4)

    if lastState['pickUp'] and lastState['object'] == numObject:
        sys.exit(1)
    elif lastState['pickUp'] and lastState['object'] != numObject:
        if lastState['gripper']:
            setAngles(coordPos0[lastState['numPose']], angles)
            if angles['left_e0'] != 0.0:
                left_limb.move_to_joint_positions(angles)
                clearAngles(angles)
            time.sleep(1)

            left_gripper.open(block=False)

            lastState['gripper'] = False

            with open(coordPath['lastState'], 'w') as jsonFile:
                json.dump(lastState, jsonFile, indent=4)

            setAngles(coordPos1[lastState['numPose']], angles)
            if angles['left_e0'] != 0.0:
                left_limb.move_to_joint_positions(angles)
                clearAngles(angles)
            time.sleep(1)

    setAngles(initData[0], angles)
    if angles['left_e0'] != 0.0:
        left_limb.move_to_joint_positions(angles)
        clearAngles(angles)
    time.sleep(1)

    cm = camModule("left")
    image = cm.getImage()
    time.sleep(5)

    
    cord = DtD.getCoordinates(image)
    cv2.rectangle(image, (cord[1], cord[3]), (cord[2], cord[4]), (255,0,0), 1)
    # cv2.imshow("",image)

    cordO1  = DtObj1.getCoordinates(image)
    cv2.rectangle(image, (cordO1[1], cordO1[3]), (cordO1[2], cordO1[4]), (0,255,0), 1)
    # cv2.imshow("1",image)

    cordO2  = DtObj2.getCoordinates(image)
    cv2.rectangle(image, (cordO2[1], cordO2[3]), (cordO2[2], cordO2[4]), (0,0,255), 1)

    if numObject == 1:
        numPose = DtGetNumPosition(cord, cordO1)
    elif numObject == 2:
        numPose = DtGetNumPosition(cord, cordO2)
    else: 
        sys.exit(1)

    adressPose = numPose.getNumPosition()

    setAngles(coordPos1[adressPose], angles)
    time.sleep(1)
    if angles['left_e0'] != 0.0:
        angles['left_w2'] = angles['left_w2']
        left_limb.move_to_joint_positions(angles)
        clearAngles(angles)

    setAngles(coordPos0[adressPose], angles)
    time.sleep(1)
    if angles['left_e0'] != 0.0:
        angles['left_w2'] = angles['left_w2']
        left_limb.move_to_joint_positions(angles)
        clearAngles(angles)

    left_gripper.close(block=False)

    setAngles(coordPos1[adressPose], angles)
    time.sleep(1)
    if angles['left_e0'] != 0.0:
        angles['left_w2'] = angles['left_w2']
        left_limb.move_to_joint_positions(angles)
        clearAngles(angles)

    lastState['pickUp'] = True
    lastState['gripper'] = True
    lastState['numPose'] = adressPose
    lastState['object'] = numObject

    with open(coordPath['lastState'], 'w') as jsonFile:
        json.dump(lastState, jsonFile, indent=4)
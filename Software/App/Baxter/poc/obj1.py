#!/usr/bin/python3

import cv2
import sys
import torch
import numpy as np 
import onnx
import onnxruntime as rt
from dataclasses import dataclass
import imutils

# import rospy
# import time
import json
import sys
import os.path
from put import exists

# # baxter_interface - Baxter Python API
# # import baxter_interface
# from baxter_interface import Limb
# from baxter_interface import Gripper

# from multiprocessing.connection import wait
# import os
# import cv2, cv_bridge 
# from baxter_interface.camera import CameraController

# from baxter_core_msgs.srv import (
#     CloseCamera,
#     ListCameras,
#     OpenCamera,
# )

# from sensor_msgs.msg import Image
# from std_msgs.msg import Bool

# from DtCameraBaxter import camModule

from DtDetection import DtDetection

coordPath = {   "init": "./initPos.json", 
                "pose0": "./Pose0.json",
                "pose1": "./Pose1.json", 
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


# def exists(path):
#     try:
#         os.stat(path)
#     except OSError:
#         return False
#     return True

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
    # DtD     = DtDetection('roboBaxter.onnx', "../../../ThirdParty/yolov5")
    # DtObj1  = DtDetection('object1.onnx', "../../../ThirdParty/yolov5")
    # DtObj2  = DtDetection('object2.onnx', "../../../ThirdParty/yolov5")
    # # DtObj1  = DtDetection('object2.onnx', "../../../ThirdParty/yolov5")
    # # image   = cv2.imread('./../poc/dataset/image13.jpg')
    # image   = cv2.imread('./test.jpg')

    # cord    = DtD.getCoordinates(image)
    # cv2.rectangle(image, (cord[1], cord[3]), (cord[2], cord[4]), (255,0,0), 1)
    # # cv2.imshow("",image)

    # cordO1  = DtObj1.getCoordinates(image)
    # cv2.rectangle(image, (cordO1[1], cordO1[3]), (cordO1[2], cordO1[4]), (0,255,0), 1)

    # # cv2.imshow("1",image)

    # cordO2  = DtObj2.getCoordinates(image)
    # cv2.rectangle(image, (cordO2[1], cordO2[3]), (cordO2[2], cordO2[4]), (0,0,255), 1)

    # cv2.imshow("2",image)
    # cv2.waitKey(0)

    # cordO2  = DtObj2.getCoordinates(image)

    # print(getNumPosition(cord, cordO2))

    coordPath = {   "init": "./initPos.json", 
                "pose0": "./Pose0.json",
                "pose1": "./Pose1.json",
                "lastState": "./lastState.json" 
            }

    lastState = {
        'pickUp': False,
        'gripper': False,
        'rotation': 0.0,
        'numPose' : 0,
        'object'  : 0
    }

    if exists(coordPath['lastState']):
        with open(coordPath['lastState'], 'r') as jsonFile:
            lastState = json.load(jsonFile)
            print(lastState)
    else:
        with open(coordPath['lastState'], 'w') as jsonFile:
            json.dump(lastState, jsonFile, indent=4)
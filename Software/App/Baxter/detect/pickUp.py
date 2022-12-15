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
    """ path check function

    Args:
        path (_type_): _description_

    Returns:
        _type_: _description_
    """
    try:
        os.stat(path)
    except OSError:
        return False
    return True

def setAngles(data, angles):
    """ function to fill angle values from coordinate dataset

    Args:
        data (_type_): _description_
        angles (_type_): _description_
    """
    j = 2
    for i in angles.keys():
        angles[i] = data[j]
        j += 1
    print(angles)

def clearAngles(angles):
    """ function to reset the state of the angles

    Args:
        angles (_type_): _description_
    """
    for i in angles.keys():
        angles[i] = 0.0




def detect(numObject:int = 1):

    global initData
    global coordPos0
    global coordPos1    

    # create instances of classes for detection and pass trained models to them.
    DtD     = DtDetection(os.path.join(dirname, './models/roboBaxter.onnx'), "/home/lev/BaxterRobo/yolov5")
    DtObj1  = DtDetection(os.path.join(dirname, './models/object1.onnx'), "/home/lev/BaxterRobo/yolov5")
    DtObj2  = DtDetection(os.path.join(dirname, './models/object2.onnx'), "/home/lev/BaxterRobo/yolov5")
    
    #create node for ros
    rospy.init_node('obj' + str(numObject), anonymous=True)


    #create an instance to control the left limb
    left_limb = Limb('left')

    #create an instance to control the left gripper
    left_gripper = Gripper('left')


    # check for exist files with coordinate dataset
    if exists(coordPath['init']) and exists(coordPath['pose0']) and exists(coordPath['pose1']):
        with open(coordPath['init'], 'r') as jsonFile:
            initData = json.load(jsonFile)
        with open(coordPath['pose0'], 'r') as jsonFile:
            coordPos0 = json.load(jsonFile)
        with open(coordPath['pose1'], 'r') as jsonFile:
            coordPos1 = json.load(jsonFile)

        if initData is None or coordPos0 is None or coordPos1 is None:
            sys.exit(1)
    else:
        print("Error")
        sys.exit(1)

    # check for exist files with last state
    if exists(coordPath['lastState']):
        with open(coordPath['lastState'], 'r') as jsonFile:
            lastState = json.load(jsonFile)
            print(lastState)
    else:
        with open(coordPath['lastState'], 'w') as jsonFile:
            json.dump(lastState, jsonFile, indent=4)


    if lastState['pickUp'] and lastState['object'] == numObject:
        # if the robot is already in the requested state, then do nothing
        sys.exit(1)
    elif lastState['pickUp'] and lastState['object'] != numObject:
        # if the robot holds another object in its grip, 
        # then first you need to put it in its original position
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

    # move the robot to the init coordinates
    setAngles(initData[0], angles)
    if angles['left_e0'] != 0.0:
        left_limb.move_to_joint_positions(angles)
        clearAngles(angles)
    time.sleep(1)

    # create a camera instance
    cm = camModule("left")
    time.sleep(5) 

    # get image from camera
    image = cm.getImage()
    time.sleep(1) 

    # get the bounding box of the grid
    cord = DtD.getCoordinates(image)
    cv2.rectangle(image, (cord[1], cord[3]), (cord[2], cord[4]), (255,0,0), 1)
    # cv2.imshow("",image)

    # get the bounding box of obj1
    cordO1  = DtObj1.getCoordinates(image)
    cv2.rectangle(image, (cordO1[1], cordO1[3]), (cordO1[2], cordO1[4]), (0,255,0), 1)
    # cv2.imshow("1",image)
    
    # get the bounding box of obj2
    cordO2  = DtObj2.getCoordinates(image)
    cv2.rectangle(image, (cordO2[1], cordO2[3]), (cordO2[2], cordO2[4]), (0,0,255), 1)

    if numObject == 1:
        numPose = DtGetNumPosition(cord, cordO1)
    elif numObject == 2:
        numPose = DtGetNumPosition(cord, cordO2)
    else: 
        print("Invalid object number")
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
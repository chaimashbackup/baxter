#!/usr/bin/python3

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
            return self.image
        else:
            print("image not found")
            return None

    def saveImage(self, name):
        if self.image is not None:
            cv2.imwrite(name, self.image)
        else:
            print("image not found")
    

class DtDetection(object):
    """_summary_

    Args:
        object (_type_): _description_
    """
    @dataclass
    class _coord: 
        """_summary_
        """
        x1:int = None
        x2:int = None
        y1:int = None
        y2:int = None
        def clear(self):
            """_summary_
            """
            self.x1 = None
            self.y1 = None
            self.x2 = None
            self.y2 = None

    _cord = _coord()
    _confidence:float
    def __init__(self, location) -> None:
        # self._model = torch.hub.load('../../../ThirdParty/yolov5/', 'custom',
        self._model = torch.hub.load('/home/lev/BaxterRobo/yolov5', 'custom',
        path=location, source='local')
        # path='roboBaxter.onnx', source='local')

    def getCoordinates(self, image:np.ndarray):
        if image is not None:
            result = self._model(image)
            if result.xyxy[0].size()[0] != 0:
                print(result.pandas().xyxy[0])
                self._cord.x1 = int(result.xyxy[0][0][0].item())
                self._cord.y1 = int(result.xyxy[0][0][1].item())
                self._cord.x2 = int(result.xyxy[0][0][2].item())
                self._cord.y2 = int(result.xyxy[0][0][3].item())
                return True, self._cord
        self._cord.clear()
        return False, self._cord


cx = 0.0
cy = 0.0

gridW = 0.0
gridH = 0.0

sector7W = 0.0
sector8W = 0.0
sectorH = 0.0

if __name__ == '__main__':
    DtD = DtDetection('roboBaxter.onnx')
    DtObj1 = DtDetection('object1.onnx')

    rospy.init_node('obj1', anonymous=True)
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


    if initData is not None and coordPos0 is not None and coordPos1 is not None:
        setAngles(initData[0], angles)
        if angles['left_e0'] != 0.0:
            # angles['left_w2'] = 0.0
            left_limb.move_to_joint_positions(angles)
            clearAngles(angles)
        time.sleep(1)
        imageGrid = camModule.getImage()
        if imageGrid is None:
            sys.exit(1)
        
        cord = DtD.getCoordinates(imageGrid)
        if cord[0] is True:
            print(cord[1])
            # cy = (cord[1].y1 + cord[1].y2) / 2
            # cx = (cord[1].x1 + cord[1].x2) / 2
            gridW = cord[1].x2 - cord[1].x1 
            gridH = cord[1].y2 - cord[1].y1 
            sector7W = gridW / 7
            sector8W = gridW / 8
            sectorH = gridH / 7
        else:
            print("grid not found")
            sys.exit(1)
        
        cordObj = DtObj1.getCoordinates(imageGrid)
        if cordObj[0] is True:
            print(cordObj[1])
            cy = (cordObj[1].y1 + cordObj[1].y2) / 2
            cx = (cordObj[1].x1 + cordObj[1].x2) / 2
        else:
            print("object1  not found")
            sys.exit(1)

        numSectorH = 0
        numSectorW = 0
        if cx <= cord[1].x2 and cx >= cord[1].x1 and cy <= cord[1].y2 and cy >= cord[1].y1:
            for i in range(7): 
                if cy < (cord[1].y1 + i * sectorH):
                    numSectorH = i
                    break

            for i in range(7): 
                if cx < (cord[1].x1 + i * sector7W):
                    numSectorW = i
                    break
            
        else:
            print("wrong dimensions")
            sys.exit(1)

        setAngles(coordPos1[numSectorH*7 + 8 - numSectorW], angles)
        time.sleep(1)
        if angles['left_e0'] != 0.0:
            angles['left_w2'] = angles['left_w2']
            left_limb.move_to_joint_positions(angles)
            clearAngles(angles)
        
        setAngles(coordPos0[numSectorH*7 + 8 - numSectorW], angles)
        time.sleep(1)
        if angles['left_e0'] != 0.0:
            angles['left_w2'] = angles['left_w2']
            left_limb.move_to_joint_positions(angles)
            clearAngles(angles)

        left_gripper.close(block=False)
        time.sleep(1)

        setAngles(coordPos1[numSectorH * 7 + 8 - numSectorW], angles)
        time.sleep(1)
        if angles['left_e0'] != 0.0:
            angles['left_w2'] = angles['left_w2']
            left_limb.move_to_joint_positions(angles)
            clearAngles(angles)

        time.sleep(5)

        setAngles(coordPos0[numSectorH*7 + 8 - numSectorW], angles)
        time.sleep(1)
        if angles['left_e0'] != 0.0:
            angles['left_w2'] = angles['left_w2']
            left_limb.move_to_joint_positions(angles)
            clearAngles(angles)

        left_gripper.open(block=False)

        setAngles(coordPos1[numSectorH * 7 + 8 - numSectorW], angles)
        time.sleep(1)
        if angles['left_e0'] != 0.0:
            angles['left_w2'] = angles['left_w2']
            left_limb.move_to_joint_positions(angles)
            clearAngles(angles)
        
        setAngles(initData[0], angles)
        if angles['left_e0'] != 0.0:
            # angles['left_w2'] = 0.0
            left_limb.move_to_joint_positions(angles)
            clearAngles(angles)
    else:
        print("wrong json file")
        sys.exit(1)
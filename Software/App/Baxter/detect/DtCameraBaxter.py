#!/usr/bin/python3

import cv2, cv_bridge 
import rospy
import time
import sys
import os.path

from baxter_interface.camera import CameraController

from baxter_core_msgs.srv import (
    CloseCamera,
    ListCameras,
    OpenCamera,
)

from sensor_msgs.msg import Image
from std_msgs.msg import Bool


class camModule(object):
    """ class for working with a Baxter camera

    Args:
        object (_type_): _description_

    Returns:
        _type_: _description_
    """
    __camName = { 'left': '/cameras/left_hand_camera/image', 'right': '/cameras/right_hand_camera/image'}
    __bridge = cv_bridge.CvBridge() 
    image = None
    def __init__(self, camName:str = 'left') -> None:
        
        rospy.Subscriber(self.__camName[camName], Image, self.camAction)

    def camAction(self, data):
        """_summary_

        Args:
            data (_type_): _description_
        """
        self.image = self.__bridge.imgmsg_to_cv2(data, desired_encoding="passthrough")

    def getImage(self):
        """ function to get image from Baxter camera module

        Returns:
            _type_: _description_
        """
        if self.image is not None:
            return self.image
        else:
            print("image not found")
            return None

    def saveImage(self, name):
        """ function to save the image received from the camera

        Args:
            name (_type_): _description_
        """
        if self.image is not None:
            cv2.imwrite(name, self.image)
        else:
            print("image not found")
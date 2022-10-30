#!/usr/bin/python3


from multiprocessing.connection import wait
import rospy
import sys
import os
import time
import cv2, cv_bridge 
from baxter_interface.camera import CameraController

from baxter_core_msgs.srv import (
    CloseCamera,
    ListCameras,
    OpenCamera,
)

from sensor_msgs.msg import Image
from std_msgs.msg import Bool


class camModule():
    bridge = cv_bridge.CvBridge() 
    image = None
    def __init__(self) -> None:
        rospy.Subscriber('/cameras/left_hand_camera/image', Image, self.amAction)

    def camAction(self, data):
        self.image = self.bridge.imgmsg_to_cv2(data, desired_encoding="passthrough")

    def getImage(self, name):
        if self.image is not None:
            cv2.imwrite(name, self.image)
        else:
            print("image not found")

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

bridge = cv_bridge.CvBridge() 
filename = 'cam0.jpg'


def camActivate(im):
    cv_image = bridge.imgmsg_to_cv2(im, desired_encoding="passthrough")
    #cv2.imshow('cam', cv_image) 
    cv2.imwrite(filename, cv_image)
    #cv2.waitKey(1)

def checkMoving(data):
    rospy.loginfo("%s",data)
    print(data)     



if __name__ == '__main__':
    rospy.init_node('camControl', anonymous=True) 
    # camActivate('right_hand_camera',(1280,800))
    # list_svc = rospy.ServiceProxy('/cameras/list', ListCameras)
    # print(list_svc)
    rospy.Subscriber('/cameras/left_hand_camera/image', Image, camActivate)

    rospy.spin() 
    #cv2.destroyAllWindows() 

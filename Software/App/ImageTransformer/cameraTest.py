#!/usr/bin/python3


import rospy
from baxter_interface.camera import CameraController


def camActivate(camera, res):
    if not any((res[0] == r[0] and res[1] == r[1]) for r in CameraController.MODES):
        rospy.logerr("Invalid resolution provided.")
    
    cam = CameraController(camera) 
    cam.resolution = res 
    cam.open() 



if __name__ == '__main__':
 rospy.init_node('camControl', anonymous=True) 
 camActivate('right_hand_camera',(1280,800))
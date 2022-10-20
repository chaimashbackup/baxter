#!/usr/bin/python3

# rospy - ROS Python API
import rospy
import rospkg
import baxter_interface

from sensor_msgs.msg import (
    Range
)

irLeftRange = Range()
irRightRange = Range()


def rightHandIR(data):
    name = 'right'	
    if (data.range != irRightRange.range):
        irRightRange.range = data.range
        rospy.loginfo("%s hand range = %s", name, irRightRange.range)

def leftHandIR(data):
    name = 'left'
    if (data.range != irLeftRange.range):
        irLeftRange.range = data.range
        rospy.loginfo("%s hand range = %s", name, irLeftRange.range)

def irtest():
    rospy.init_node('ir', anonymous=True)
    rospy.Subscriber("/robot/range/left_hand_range/state", Range, leftHandIR)
    rospy.Subscriber("/robot/range/right_hand_range/state", Range, rightHandIR)
    rospy.spin()

if __name__=='__main__':
    print("start ir test")
    irtest()



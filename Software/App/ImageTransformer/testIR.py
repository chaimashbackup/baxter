#!/usr/bin/python3

# rospy - ROS Python API
import rospy
import rospkg
import baxter_interface

from sensor_msgs.msg import (
    Range
)

irRange = Range()

def callback(data):
    if (data.range != irRange.range):
        irRange.range = data.range
        rospy.loginfo("Range = %s",irRange.range)

def irtest():
    rospy.init_node('ir', anonymous=True)
    rospy.Subscriber("/robot/range/right_hand_range/state", Range, callback)
    rospy.spin()

if __name__=='__main__':
    print("start ir test")
    irtest()



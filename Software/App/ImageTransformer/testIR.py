#!/usr/bin/python3

# rospy - ROS Python API
import rospy
import rospkg

import baxter_interface

from sensor_msgs.msg import (
    Range,
    String
)


def callback(data):
    rospy.loginfo(rospy.get_name() + ": Range = %f" % data.range)

def irtest():
    rospy.init_node('ir', anonymous=True)
    rospy.Subscriber("/robot/range/left_hand_range", Range, callback)
    rospy.spin()

if __name__=='__main__':
    irtest()



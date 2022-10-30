#!/usr/bin/python3

# rospy - ROS Python API
import rospy
import rospkg
import baxter_interface

from sensor_msgs.msg import (
    Range
)

class irModule():
    irRange = Range()
    def __init__(self) -> None:
        # rospy.init_node('IR', anonymous=True)
        rospy.Subscriber("/robot/range/left_hand_range/state", Range, self.leftHandIR)
        

    def leftHandIR(self, data):
        if (data.range != self.irRange.range):
            self.irRange = data
            # rospy.loginfo("%s hand range = %s", "left IR", self.irRange.range)

    def getRange(self):
        if self.irRange is None:
            return 0
        else:
            return self.irRange.range

    def getLimit(self):
        return self.irRange.max_range, self.irRange.min_range
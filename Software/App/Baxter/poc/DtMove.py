import rospy 
import sys
import struct
import moveit_commander

from geometry_msgs.msg import (
    Quaternion
)

import baxter_interface
from baxter_core_msgs.srv import (
    SolvePositionIK,
    SolvePositionIKRequest)

class DtMove():
    _ikService = None
    _guaterion = None

    def __init__(self) -> None:
        self._ikService = rospy.ServiceProxy("ExternalTools/left/PositionKinematicsNode/IKService", SolvePositionIK)


    def move(self, nameLimb, goal, timeout):
        ikRequest = SolvePositionIKRequest()
        self._guaterion = Quaternion()

        mvP = struct.pack('??', True, False)

        mvP.find()





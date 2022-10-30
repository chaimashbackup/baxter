import rospy

import std_msgs
import baxter_interface
import moveit_commander
import sensor_msgs
import geometry_msgs

import irModule
from baxterMove import baxterMove


def initPose():
    leftInitState = {
        'left_e0': -1.1884516154142244,
        'left_e1': 1.9378012302962488,
        'left_s0': -0.08206797215186963,
        'left_s1': -0.998237997716433,
        'left_w0': 0.668432128321069,
        'left_w1': 1.0270001374892845,
        'left_w2': -0.5019952128355016
    }
    limb = baxter_interface.Limb('left')
    limb.move_to_joint_positions(leftInitState)



if __name__ == '__main__':

    # rospy.init_node('planning', log_level=rospy.INFO)
    bm = baxterMove()
    initPose()
    bm.setPose(0.1, 0.1, 0.1)

from xml.etree.ElementInclude import LimitedRecursiveIncludeError
import rospy

import time
import std_msgs
import baxter_interface
import moveit_commander
import sensor_msgs
import geometry_msgs

import irModule
from baxterMove import baxterMove
from camModule import camModule
from irModule import irModule
from DtGripper import DtGripper


from sensor_msgs.msg import (
    JointState
)

leftInitState = {
    'left_e0': -1.1884516154142244,
    'left_e1': 1.9378012302962488,
    'left_s0': -0.08206797215186963,
    'left_s1': -0.998237997716433,
    'left_w0': 0.668432128321069,
    'left_w1': 1.0270001374892845,
    'left_w2': -0.5019952128355016
}

def initPose():

    limb = baxter_interface.Limb('left')
    limb.move_to_joint_positions(leftInitState)

def cb(data):
    print(data)

if __name__ == '__main__':
    
    rospy.init_node('planning', log_level=rospy.INFO)
    # initPose()
    bm = baxterMove() 
    # cm = camModule()
    # ir = irModule()

    # time.sleep(3)
    # lenthIR = ir.getRange()
    # limit = ir.getLimit()
    # print(ir.getRange())
    # print(ir.getLimit())

    # lim = 0.30
    # while ir.getRange() >= lim:
    #     if ir.getRange() > limit[0]:
    #         bm.setPose(0.0, 0.0, -0.05)
    #     else:
    #         bm.setPose(0, 0.0, lim - ir.getRange())
    #     lenthIR = ir.getLimit()


    # i = 0
    # while i <= 5:
    #     time.sleep(1)
    #     cm.getImage("image" + str(i) + ".jpg")
    #     bm.setPose(0.0, 0.0, -0.05)
    #     print(ir.getRange())
    #     i+=1

    # bm.setPose(0.0, 0.0, 0.1)
    # time.sleep(5)
    # bm.setPose(0.0, 0.0, 0.1)
    # initPose()

    # gr = DtGripper()
    # gr.command(0, 100.0, 10.0)
    # gr.wait(0)
    # rospy.spin()


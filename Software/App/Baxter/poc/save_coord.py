import rospy
import baxter_interface

import json
import sys
import os.path

from sensor_msgs.msg import (
    JointState
)



data = []
path = "./coord2.json"
chek = True
# limb_left = baxter_interface.Limb("left")

def exists(path):
    try:
        os.stat(path)
    except OSError:
        return False
    return True
pos = None

def cb(data):
    global pos
    if pos is None:
        pos = data.position
        print(pos)
        global chek
        chek = False
    if pos != data.position:
        pos = data.position
        # print(pos)

if __name__ == '__main__':
    rospy.init_node('save_coord', anonymous=True)
    rospy.Subscriber("/robot/joint_states", JointState, cb)
    while chek:
        pass

    if exists(path):
        with open(path, 'r') as jsonFile:
            data = json.load(jsonFile)
            
    data.append(pos)
    with open(path, 'w') as jsonFile:
        json.dump(data, jsonFile, indent=4)



    # rospy.spin()

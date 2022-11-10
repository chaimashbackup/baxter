import rospy
import baxter_interface

import json
import sys
import os.path

left_hand_default_angles = {
    'left_e0': -1.1884516154142244,
    'left_e1': 1.9378012302962488,
    'left_s0': -0.08206797215186963,
    'left_s1': -0.998237997716433,
    'left_w0': 0.668432128321069,
    'left_w1': 1.0270001374892845,
    'left_w2': -0.5019952128355016
}

data = []
path = "./file.json"

limb_left = baxter_interface.Limb("left")

def exists(path):
    try:
        os.stat(path)
    except OSError:
        return False
    return True

if __name__ == '__main__':

    joints_left = limb_left.joint_names()
    if exists(path):
        with open(path, 'r') as jsonFile:
            data = json.load(jsonFile)
            
    data.append(left_hand_default_angles)
    with open(path, 'w') as jsonFile:
        json.dump(data, jsonFile, indent=4)
    for i in data:
        print("-----")
        print(i)
        print("-----")

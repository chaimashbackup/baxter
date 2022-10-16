#!/bin/bash

if [ "${1}" = "list" ]
then
    rosrun baxter_tools camera_control.py -l
elif [ "${1}" = "enumerate" ]
then
    rosrun baxter_tools camera_control.py -e
elif [ "${1}" = "open" ]
then
    rosrun baxter_tools camera_control.py -o "${2}"
elif [ "${1}" = "close" ]
then
    rosrun baxter_tools camera_control.py -c "${2}"
else
    echo "Unknown command. Use list|enumerate|open <CAMERA>|close <CAMERA>."
    echo "Where CAMERA is either head_camera, left_hand_camera or right_hand_camera."
fi
